from datetime import datetime, time
from pytz import timezone
from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    total_attendance_hours = fields.Float(
        string="Total Attendance Hours",
        compute="_compute_total_attendance_hours",
        store=True,
        help="Total attendance hours during the payslip period.",
    )
    num_of_days = fields.Float(
        string="Number of Days",
        compute="_compute_sum",
        store=True,
        help="Total Worked Days",
    )

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_total_attendance_hours(self):
        for payslip in self:
            if not (payslip.employee_id and payslip.date_from and payslip.date_to):
                payslip.total_attendance_hours = 0
                continue

            # Fetch total attendance hours for the employee in the payslip period
            total_hours = self.get_attendance_hours(payslip.employee_id.id, payslip.date_from, payslip.date_to)
            payslip.total_attendance_hours = total_hours

    @api.model
    def get_attendance_hours(self, employee_id, date_from, date_to):
        """
        Fetch and compute total attendance hours for an employee within a given date range.
        This method can be used independently of the payslip model.
        """
        # Fetch attendance records for the employee within the date range
        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', employee_id),
            ('check_in', '>=', date_from),
            ('check_out', '<=', date_to)
        ])

        # Sum the worked_hours fetched from the attendance
        total_hours = sum(
            round(attendance.worked_hours, 2)
            for attendance in attendances if attendance.worked_hours
        )

        return total_hours

    def get_worked_day_lines(self, contracts, date_from, date_to):
        res = []
        global_leaves = {}  # This will store the accumulated public holidays
        leaves = {} # This will store leave types other than holidays

        # Process each contract with a working schedule
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)  # The timezone of the employee's calendar

            # Convert the date_from and date_to to datetime objects with timezone
            date_from_dt = tz.localize(datetime.combine(date_from, time.min)) if date_from else None
            date_to_dt = tz.localize(datetime.combine(date_to, time.max)) if date_to else None

            # Calculate total attendance hours for the employee in the given period
            total_hours = self.get_attendance_hours(contract.employee_id.id, date_from_dt, date_to_dt)

            # Calculate total days based on attendance
            work_hours = 8
            total_days = total_hours / work_hours

            # Attendance entry
            attendances = {
                'name': _("Normal Working Days paid at 100%"),
                'sequence': 1,
                'code': 'WORK100',
                'number_of_days': total_days,  # Only attendance days
                'number_of_hours': total_hours,
                'contract_id': contract.id,
                'time_type': 'attendance'
            }

            # Fetch leave data (approved leaves)
            day_leave_intervals = self.env['hr.leave'].search([
                ('employee_id', '=', contract.employee_id.id),
                ('state', '=', 'validate'),  # Ensure only approved leaves are considered
                ('date_from', '<=', date_to_dt),
                ('date_to', '>=', date_from_dt),
            ])

            # Process employee-specific leaves
            for leave in day_leave_intervals:
                leave_duration_days = leave.number_of_days  # Total days for the leave
                leave_duration_hours = leave.number_of_hours  # Total hours for the leave

                # Convert leave's date_from and date_to to timezone-aware datetime objects
                leave_date_from_dt = tz.localize(
                    leave.date_from) if leave.date_from and leave.date_from.tzinfo is None else leave.date_from
                leave_date_to_dt = tz.localize(
                    leave.date_to) if leave.date_to and leave.date_to.tzinfo is None else leave.date_to

                # Check if the leave falls within the date range
                if leave_date_to_dt >= date_from_dt and leave_date_from_dt <= date_to_dt:
                    # Ensure each leave type is handled separately
                    holiday_status = leave.holiday_status_id
                    leave_struct = leaves.setdefault(holiday_status, {
                        'name': holiday_status.name or _('Global Leaves'),
                        'sequence': 5,
                        'code': holiday_status.code or 'GLOBAL',
                        'number_of_days': 0.0,
                        'number_of_hours': 0.0,
                        'contract_id': contract.id,
                        'time_type': holiday_status.time_type
                    })

                    # Add the leave duration to the leave structure
                    leave_struct['number_of_hours'] += leave_duration_hours
                    leave_struct['number_of_days'] += leave_duration_days

            # # Fetch mandatory days
            # mandatory_days = self.env['hr.leave.mandatory.day'].search([
            #     ('start_date', '<=', date_to_dt),
            #     ('end_date', '>=', date_from_dt),
            # ])
            #
            # # Initialize variables to accumulate mandatory days total
            # total_mandatory_days = 0
            # total_mandatory_hours = 0
            #
            # for mandatory_day in mandatory_days:
            #     mandatory_start_date = mandatory_day['start_date']
            #     mandatory_end_date = mandatory_day['end_date']
            #
            #     # Calculate the number of days for each mandatory day
            #     mandatory_day_calc = (mandatory_end_date - mandatory_start_date).days
            #
            #     total_mandatory_days += mandatory_day_calc
            #     total_mandatory_hours += mandatory_day_calc * 8  # Assuming 8 hours per mandatory day
            #
            # # Create a single entry for all mandatory days
            # if total_mandatory_days > 0:
            #     mandatory_day_struct = leaves.setdefault('MANDATORY_DAYS', {
            #         'name': _("Mandatory Days"),
            #         'sequence': 15,
            #         'code': 'MANDATORY_DAY',
            #         'number_of_days': total_mandatory_days,
            #         'number_of_hours': total_mandatory_hours,
            #         'contract_id': contract.id,
            #         'time_type': 'general'
            #     })

            # Fetch public holidays
            public_holidays = self.env['resource.calendar.leaves'].search([
                ('date_from', '<=', date_to_dt),
                ('resource_id', '=', False),
                ('time_type', '=', 'leave'),
                ('calendar_id', '=', False)  # Public holidays usually have no specific calendar
            ])

            # Initialize variables to store holiday details
            total_holiday_days = 0
            total_holiday_hours = 0

            # Process each holiday found
            for holiday in public_holidays:
                # Access the dates
                start_date = fields.Datetime.from_string(holiday.date_from)
                end_date = fields.Datetime.from_string(holiday.date_to)

                # Calculate the holiday duration in days and hours
                holiday_duration_days = (end_date - start_date).days + 1  # Inclusive of both start and end dates
                holiday_duration_hours = holiday_duration_days * 8  # Assuming an 8-hour workday

                # Accumulate the totals
                total_holiday_days += holiday_duration_days
                total_holiday_hours += holiday_duration_hours

            # If holidays are found, create a structured entry for them
            if total_holiday_days > 0:
                global_leaves['GLOBAL LEAVES'] = {
                    'name': _("Global Leaves"),
                    'sequence': 20,
                    'code': 'Global',
                    'number_of_days': total_holiday_days,
                    'number_of_hours': total_holiday_hours,
                    'contract_id': contract.id,  # Ensure contract context is available
                    'time_type': 'general'
                }

            # Append attendance and leave data to the result
            res.append(attendances)
            res.extend(leaves.values())  # Add individual leave entries
            res.extend(global_leaves.values())  # Add the global holiday entry

        return res

    @api.depends('employee_id', 'date_from', 'date_to', 'total_attendance_hours')
    def _compute_sum(self):
        for payslip in self:
            if not payslip.employee_id:
                continue  # Avoid processing if there's no employee

            # Check if the employee_id has changed
            if payslip.employee_id != payslip._origin.employee_id:
                payslip.worked_days_line_ids = [(5, 0, 0)]  # Clear old worked days lines

            # Get the current employee's contract
            contracts = payslip.employee_id.contract_id
            worked_day_lines = self.get_worked_day_lines(
                contracts, payslip.date_from, payslip.date_to
            )

            # Initialize a list to track lines to be updated or appended
            worked_day_line_vals = []

            if worked_day_lines:
                for line in worked_day_lines:
                    # Check if the line already exists in the payslip's worked_days_line_ids
                    existing_line = next(
                        (existing for existing in payslip.worked_days_line_ids if existing.code == line.get('code')),
                        None)

                    if existing_line:
                        # If line exists, update it
                        existing_line.number_of_days = line.get('number_of_days')
                        existing_line.time_type = line.get('time_type')
                    else:
                        # If line doesn't exist, append a new line
                        worked_day_line_vals.append((0, 0, line))

                # Update only the new or modified lines without clearing the old ones
                if worked_day_line_vals:
                    payslip.write({'worked_days_line_ids': [(5, 0, 0)] + worked_day_line_vals})

                # Calculate the total worked days, considering leave days
                total_worked_days = 0
                for line in worked_day_lines:

                    # if 'time_type' in line:
                    #     if line['time_type'] == 'leave':
                    #         total_worked_days -= line['number_of_days']
                    #     elif line['time_type'] == 'other' and line['name'] != 'Global Leaves':
                    #         total_worked_days += line['number_of_days']
                    # elif line['name'] != 'Mandatory Days':
                    #     total_worked_days += line['number_of_days']
                    if line['time_type'] in ['attendance','other','general']:
                        total_worked_days += line['number_of_days']
                    # elif line['time_type'] == 'leave':
                        # total_worked_days -= line['number_of_days']
                    else:
                        continue

                payslip.num_of_days = total_worked_days
            else:
                # If no worked day lines are found, ensure num_of_days is set to 0
                payslip.num_of_days = 0



class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    time_type = fields.Char()
    num_of_days = fields.Float(
        string="Number of Days",
        store=True
    )


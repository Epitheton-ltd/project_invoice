# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


__all__ = ['TimesheetLine']


class TimesheetLine(metaclass=PoolMeta):
    __name__ = 'timesheet.line'
    invoice_line = fields.Many2One('account.invoice.line', 'Invoice Line',
        readonly=True)

    @classmethod
    def __setup__(cls):
        super(TimesheetLine, cls).__setup__()
        cls._error_messages.update({
                'modify_invoiced_line': 'You can not modify invoiced line.',
                'delete_invoiced_line': 'You can not delete invoiced line.',
                })

    @classmethod
    def copy(cls, records, default=None):
        if default is None:
            default = {}
        else:
            default = default.copy()
        default.setdefault('invoice_line', None)
        return super(TimesheetLine, cls).copy(records, default=default)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        for lines, values in zip(actions, actions):
            if (('duration' in values or 'work' in values)
                    and any(l.invoice_line for l in lines)):
                cls.raise_user_error('modify_invoiced_line')
        super(TimesheetLine, cls).write(*args)

    @classmethod
    def delete(cls, records):
        if any(r.invoice_line for r in records):
            cls.raise_user_error('delete_invoiced_line')
        super(TimesheetLine, cls).delete(records)

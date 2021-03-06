# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _gen_fiskal_number(self, invoice, move):
        prostor = invoice.fiskal_uredjaj_id.prostor_id.oznaka_prostor
        uredjaj = str(invoice.fiskal_uredjaj_id.oznaka_uredjaj)
        # DB: Refund sequence je isti kao i main seq osim ako nije drugačije zadano!
        separator = invoice.company_id.fiskal_separator
        sequence = move.journal_id.sequence_id
        pref, suff = sequence.prefix, sequence.suffix
        broj = move.name
        blen = len(broj)
        for where in [pref, suff]:
            if not where or where == '':
                continue
            for what in ['%(range_year)s', '%(year)s']:
                # TODO : ostali formati
                if what in where:
                    where = where.replace(what, str(invoice.date_invoice)[:4])
            broj = broj.replace(where, '')
            if len(broj) < blen:
                blen = len(broj)
            else:
                raise ValidationError('Prefix ili sufix brojevnog kruga nije podržan!')
        fiskalni_broj = separator.join((str(int(broj)), prostor, uredjaj))
        if not invoice.fiskalni_broj:
            invoice.fiskalni_broj = fiskalni_broj
        # else:
        #     invoice.comment = invoice.comment and invoice.comment + '\n' or '' + \
        #                       ' Prilikom potvrđivanja računa korišten je importirani broj računa'


    @api.multi
    def post(self):
        res = super(AccountMove, self).post()
        invoice = self.env.context.get('invoice', False)
        if invoice and invoice.type in ('out_invoice', 'out_refund'):
            for move in self:
                if not move.company_id.croatia:
                    continue
                # only for croatia invoices i check active premise
                if invoice.fiskal_uredjaj_id.prostor_id.state != 'active':
                    raise ValidationError(_("Invoice posting not possible, business premisse is not active!"))
                self._gen_fiskal_number(invoice, move)
                #and set lock on journals, after first posting journal is locked for changes
                if not invoice.fiskal_uredjaj_id.lock:
                    invoice.fiskal_uredjaj_id.lock = True
                if not invoice.fiskal_uredjaj_id.prostor_id.lock:
                    invoice.fiskal_uredjaj_id.prostor_id.lock = True
        return res




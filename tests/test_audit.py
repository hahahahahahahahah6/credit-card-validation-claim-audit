import tempfile
import unittest
from pathlib import Path
from credit_card_validation_claim_audit.audit import audit, evidence, matches, prose
from credit_card_validation_claim_audit.phrases import CREDITCARDVALIDATION, NOCREDITCARDVALIDATION, GENERIC_NAMES

ROOT = Path(__file__).resolve().parents[1]

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        for phrase in CREDITCARDVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertTrue(matches(phrase)[0])
        for phrase in NOCREDITCARDVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertEqual(matches(phrase)[0], [])
                self.assertTrue(matches(phrase)[1])
        self.assertEqual(matches('```\nvalidate card\n```'), ([], []))

    def test_library_routes(self):
        for name in 'card_number visa mastercard amex unionpay diners jcb discover mir'.split():
            for source in ('import validators as v\nv.%s()' % name, 'from validators import %s as f\nf()' % name):
                with self.subTest(source=source): self.assertTrue(evidence(source))
        for name in 'verify checksum generate append'.split():
            for source in ('import luhn as l\nl.%s()' % name, 'from luhn import %s as f\nf()' % name):
                with self.subTest(source=source): self.assertTrue(evidence(source))
        for source in ('from creditcard import CreditCard as C\nC().is_valid', 'import creditcard as c\nx = c.CreditCard()\nx.is_valid', 'from creditcard import CreditCard\nwith CreditCard() as cc:\n    cc.is_valid'):
            with self.subTest(source=source): self.assertTrue(evidence(source))
        for name in GENERIC_NAMES:
            for source in ('x = object()\nx.%s()' % name, 'from foo import %s as f\nf()' % name):
                with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import validators', 'import creditcard', 'import luhn', 'import other', 'from creditcard import CreditCard\nCreditCard()', 'x.brand', 'x.is_valid', 'import re\nre.match("[0-9]+", x)', 'x.startswith("4")', 'import validators\nvalidators.email()', 'import validators\nvalidators.url()', 'import validators\nvalidators.ipv4()', 'import validators\nvalidators.ipv6()', 'import validators\nvalidators.domain()', 'email.validate()', 'phone.validate()', 'date.validate()', 'ip.validate()', 'url.validate()', 'payment.charge()', 'document.extract()', '"validate card"', '# validate card', 'x.validate_card', 'def broken(:', 'import subprocess\nsubprocess.run(["card-validator"])', 'from creditcard import CreditCard\nCreditCard().is_valid()', 'import validators\nvalidators = 2\nvalidators.card_number()', 'from foo import validate_card\ndef validate_card(): pass\nvalidate_card()']
        for name in 'card_number visa mastercard amex unionpay diners jcb discover mir verify checksum generate append'.split():
            cases.extend([name+'()', 'unknown.'+name+'()'])
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'README.md').write_text('validate card')
            (root/'a.py').write_text('from creditcard import CreditCard\nx = CreditCard()')
            (root/'b.py').write_text('x.is_valid')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')

    def test_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); readme=root/'README.md'; readme.write_text('validate card')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')
            (root/'test_x.py').write_text('import luhn\nluhn.verify()')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'MEDIUM')
            (root/'app.py').write_text('import validators\nvalidators.card_number()')
            self.assertEqual(audit(root)['findings'], [])
            readme.write_text('no card validation')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')

    def test_self_audit(self):
        self.assertEqual(audit(ROOT)['findings'], [])
        self.assertEqual(audit(ROOT/'README.md')['findings'], [])

    def test_limitations_prose(self):
        text=(ROOT/'README.md').read_text().split('## Limitations',1)[1]
        self.assertEqual(matches(prose(text)), ([], []))

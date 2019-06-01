import sqlalchemy as sa

import muesli
import muesli.models as models

engine = sa.create_engine('postgresql:///muesli')
muesli.engine = lambda: engine
models.initializeSession(engine)
session = models.Session()


def autoCorrectSubjects():
    def autoList(subject, right, wrongs):
        variants_post = wrongs
        format_list = ['%s %s' % (subject, postfix) for postfix in variants_post]
        variants_pre = variants_post + [right]
        format_list += ['%s %s' % (prefix, subject) for prefix in variants_pre]
        return format_list

    def autoListBSc(subject):
        return autoList(subject, '(BSc)', ['Bachelor', 'bsc', 'Bsc', 'BSc', 'B.Sc.', '(Bsc)', '(BSC.)', '(B.Sc.)'])

    def autoListMSc(subject):
        return autoList(subject, '(MSc)', ['Master', 'msc', 'Msc', 'MSc', 'M.Sc.', '(Msc)', '(BSC.)'])

    def autoListPhD(subject):
        return autoList(subject, '(PhD)', ['phd', 'Phd', 'PhD', 'phd.', 'Phd.', 'PhD.', 'Ph.D.', '(phd)', '(Phd.)'])

    def autoListDipl(subject):
        return autoList(subject, '(Dipl.)', ['Diplom', 'dipl', 'Dipl', 'Dipl.', '(Dipl)'])

    def autoListLAHaupt(subject):
        return autoList(subject, '(LA) (Hauptfach)', ['(LA) Hauptfach', 'LA, Hauptfach', '(LA Hauptfach)'])

    def autoListLABei(subject):
        return autoList(subject, '(LA) (Beifach)', ['(LA) Beifach', 'LA, Beifach', '(LA Beifach)'])

    def autoListLA(subject):
        return autoList(subject, '(LA)', ['Lehramt', '(Lehramt)', 'LA'])

    def autoListPromotion(subject):
        return autoList(subject, '(Promotion)', ['Promotion', 'dipl', 'Dipl', 'Dipl.', '(Dipl)'])

    subjects = ['Angewandte Informatik',
                'Anwendungsorientierte Informatik',
                'Biologie',
                'Biowissenschaften',
                'Economics',
                'Geowissenschaften',
                'Psychologie',
                'Chemie',
                'Computerlinguistik',
                'Geographie',
                'Informatik',
                'Molekulare Biotechnologie',
                'Molekulare Zellbiologie',
                'Mathematik',
                'Physik',
                'Philosophie',
                'Alte Geschichte',
                'Wissenschaftliches Rechnen', ]
    corrections = {}
    for subject in subjects:
        corrections['%s (BSc)' % subject] = autoListBSc(subject)
        corrections['%s (MSc)' % subject] = autoListMSc(subject)
        corrections['%s (PhD)' % subject] = autoListPhD(subject)
        corrections['%s (Dipl.)' % subject] = autoListDipl(subject)
        corrections['%s (Promotion)' % subject] = autoListPromotion(subject)
        corrections['%s (LA) (Hauptfach)' % subject] = autoListLAHaupt(subject)
        corrections['%s (LA) (Beifach)' % subject] = autoListLABei(subject)
        corrections['%s (LA)' % subject] = autoListLA(subject)
    for right, wrongs in list(corrections.items()):
        for wrong in wrongs:
            print("%s -> %s" % (wrong, right))
            correctSubjects(wrong, right)


def correctSubjects(old, new):
    us = session.query(models.User).filter(models.User.subject == old).all()
    if us:
        for u in us:
            print(u)
        answer = input("Change subject to %s? (y/N)" % new).lower()
        if answer == 'y':
            for u in us:
                u.subject = new
                print("Changed", u)
        print("Do not forget to commit")


print("A muesli-session has been initialized as 'session'")
print("The muesli models have been included via 'models'")

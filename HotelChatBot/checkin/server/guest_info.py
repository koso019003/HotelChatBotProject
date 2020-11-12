import random
import datetime

from faker import Faker
fake = Faker()


class BookingInfo:
    def __init__(self, gender='0'):
        self.gender = int(gender)  # 0 female; 1 male
        self.f_name = 'Martin'
        self.l_name = 'Sarah'

        self.a_date = datetime.datetime.now()
        self.d_date = ''

        self.res_no = '10132020'
        self.r_type = ['Standard', 'Deluxe', 'Alexander']
        self.r_rate = 400

        self.duration = 0

        self.full_name = ''

        self.random_init()

    def random_init(self):

        if self.gender:  # if gender is male
            self.f_name = fake.first_name_male()
            self.l_name = fake.last_name_male()

        else:
            self.f_name = fake.first_name_female()
            self.l_name = fake.last_name_female()

        self.duration = random.randrange(1, 10)
        self.d_date = self.a_date + datetime.timedelta(days=self.duration)

        self.a_date = self.a_date.strftime("%d %b %Y")
        self.d_date = self.d_date.strftime("%d %b %Y")

        self.res_no = ''.join([str(k) for k in random.choices(range(10), k=6)])

        self.r_type = random.choice(self.r_type)
        self.r_rate = random.randint(1, 10) * 100

        self.full_name = '{} {}'.format(self.f_name, self.l_name)

    def __str__(self):
        output = (
            'First Name: {}\t'.format(self.f_name) +
            'Last Name: {}\n'.format(self.l_name) +
            'Arrival Date: {}\n'.format(self.a_date) +
            'Departure Date: {}\n'.format(self.d_date) +
            'Reservation No.: {}\n'.format(self.res_no) +
            'Room Type: {}\t'.format(self.r_type) +
            'Room Rate: ${}\n'.format(self.r_rate)
        )
        return output


class BusinessInfo:
    def __init__(self):
        self.zip = ''
        self.country = ''
        self.address = ''

        self.email = ''
        self.phone = ''

        self.random_init()

    def random_init(self):
        self.zip = ''.join([str(k) for k in random.choices(range(10), k=6)])
        self.country = fake.country()

        _door = random.randint(11, 99)
        _addrs = ', '.join([self.country, fake.state(), self.zip])
        self.address = '#{} {}'.format(_door, _addrs)

        self.phone = '0' + ''.join([str(k) for k in random.choices(range(10), k=7)])
        self.email = '{0}{1}@{0}.com'.format(fake.first_name(),
                                             ''.join([str(k) for k in random.choices(range(10), k=3)]))

    def __str__(self):
        output = (
            'Address: {}\n'.format(self.address) +
            'Country: {}\t'.format(self.country) +
            'Zip Code: {}\n'.format(self.zip) +
            'Phone: {}\n'.format(self.phone) +
            'Email: {}\n'.format(self.email)
        )
        return output


class IdInfo:
    def __init__(self, name):
        self.full_name = name
        self.id_no = ''
        self.nationality = 'HappyLand'
        self.date_birth = datetime.date.fromisoformat('1990-10-10')

        self.date_issue = ''
        self.date_expiry = ''

        self.random_init()

    def random_init(self):

        random_number_of_days = random.randrange(1000)
        self.date_birth = self.date_birth + datetime.timedelta(days=random_number_of_days)
        self.date_issue = self.date_birth + datetime.timedelta(days=365*25 + random_number_of_days)
        self.date_expiry = self.date_issue + datetime.timedelta(days=365*10)

        self.date_birth = self.date_birth.strftime("%d%b%Y")
        self.date_issue = self.date_issue.strftime("%d%b%Y")
        self.date_expiry = self.date_expiry.strftime("%d%b%Y")

        id_no = ''.join([str(k) for k in random.choices(range(10), k=6)])
        id_no = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + id_no
        self.id_no = id_no + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def __str__(self):
        output = (
            "Full Name: {}\n".format(self.full_name) +
            "ID Number: {}\n".format(self.id_no) +
            "Nationality: {}\n".format(self.nationality) +
            "Date of Birth: {}\n".format(self.date_birth) +
            "Date of Issue: {}\n".format(self.date_issue) +
            "Date of Expiry: {}\n".format(self.date_expiry)
        )
        return output


class GuestInfo:
    """docstring for GuestInfo"""
    def __str__(self):
        output = "GuestInfo class: \n\n"
        for key, var in vars(self).items():
            output += '{}:\n{}\n'.format(str(key), str(var))
            output += '-'*10 + '\n'
        return output

    def __init__(self, gender='0'):
        self.booking_info = BookingInfo(gender=gender)
        self.business_info = BusinessInfo()
        self.id_info = IdInfo(self.booking_info.full_name)

        self.name = ' '.join([self.booking_info.f_name, self.booking_info.l_name])

        self.bag_with_self = False
        self.bags_with_porter = True
        self.luggage_help = True

        self.pay_later = False
        self.pay_later_reason = ""
        # self.pay_later_reason = [
        #     "don't have enough of money",
        #     "do not have credit card with me",
        #     "forgot to bring cash",
        #     "forgot to bring credit card"
        # ]
        self.payment = ["credit card", "cash"]
        self.payment_other = ["PayLah", "PayNow", "cheque"]

        self.purpose = ["Business", "Leisure"]

        self.receive_email = True
        self.smoke = True

        self.business_card = True

        # *** No random ***
        self.pay_overtime = True
        self.overtime_no_argue = True
        self.special_issue = False
        # *** No random ***

        self.will_over_time = True
        self.departure_time = "15"

        self.identity_document_fake = ["Credit Card", "Business Card"]
        self.identity_document_true = [
            "Passport", "Identity Card", "Driver's License"]
        self.local = True

        # initialize
        self.random_init()

    def random_init(self):
        boolean = [True, False]

        self.bag_with_self = random.choice(boolean)
        self.bags_with_porter = not self.bag_with_self
        if self.bag_with_self:
            self.luggage_help = random.choice(boolean)

        # if random.random() > 0.6:
        #     self.pay_later = True
        #     self.pay_later_reason = random.choice(self.pay_later_reason)
        # else:
        #     self.pay_later = False
        #     self.pay_later_reason = ""

        self.payment = random.choice(self.payment)
        if random.random() > 0.6:
            self.payment_other = random.choice(self.payment_other)
        else:
            self.payment_other = ''

        self.purpose = random.choice(self.purpose)

        self.receive_email = random.choice(boolean)
        self.smoke = random.choice(boolean)

        self.business_card = random.choice(boolean)

        self.will_over_time = random.choice(boolean)
        if self.will_over_time:
            self.departure_time = random.randrange(13, 16)
        else:
            self.departure_time = random.randrange(6, 12)

        self.identity_document_fake = random.choice(self.identity_document_fake)
        self.identity_document_true = random.choice(self.identity_document_true)

        if random.random() > 0.7:
            self.local = True
            self.identity_document_true = 'NRIC'
        else:
            self.local = False


if __name__ == '__main__':
    a = GuestInfo()
    print(a)
    a = vars(a.business_info)
    print(a)

import random
import datetime
from faker import Faker

fake = Faker()


class StayInfo:
    def __init__(self, gender='0'):
        self.gender = int(gender)  # 0 female; 1 male

        self.f_name = 'Martin'
        self.l_name = 'Sarah'

        self.a_date = ''
        self.d_date = datetime.datetime.now()

        self.folio_no = 'INV2189'
        self.room_num = '1618'

        self.a_c_num = '1/0'
        self.cashier_id = 'LK'
        self.page = 1

        self.print_date = self.d_date

        self.full_name = ''

        self.random_init()

    def random_init(self):

        if self.gender:  # if gender is male
            self.f_name = fake.first_name_male()
            self.l_name = fake.last_name_male()

        else:
            self.f_name = fake.first_name_female()
            self.l_name = fake.last_name_female()

        duration = random.randrange(1, 10)
        self.a_date = self.d_date - datetime.timedelta(days=duration)

        self.a_date = self.a_date.strftime("%d-%b-%Y")
        self.d_date = self.d_date.strftime("%d-%b-%Y")

        self.folio_no = 'INV{}'.format(fake.random_int(0, 9999))
        self.room_num = '{}'.format(fake.random_int(0, 9999))

        self.a_c_num = '{}/{}'.format(fake.random_int(1, 9),
                                         fake.random_int(0, 4))
        self.cashier_id = fake.random_uppercase_letter() + fake.random_uppercase_letter()
        self.page = random.randint(1, 10)
        self.print_date = self.d_date

        title = ['Mr.', 'Ms'][self.gender]
        self.full_name = '{} {} {}'.format(title, self.f_name, self.l_name)

    def __str__(self):
        output = (
                'First Name: {}\t'.format(self.f_name) +
                'Last Name: {}\n'.format(self.l_name) +
                'Arrival Date: {}\n'.format(self.a_date) +
                'Departure Date: {}\n'.format(self.d_date) +
                'Folio No.: {}\n'.format(self.folio_no) +
                'Room No.: {}\t'.format(self.room_num) +
                'Number of Adult/children: {}\n'.format(self.a_c_num) +
                'Cashier ID.: {}\t'.format(self.cashier_id) +
                'Page : {}\t'.format(self.page) +
                'Print Date: {}\t'.format(self.print_date)
        )
        return output


class GuestInfo:
    """docstring for GuestInfo"""

    def __str__(self):
        output = "GuestInfo class: \n\n"
        for key, var in vars(self).items():
            output += '{}:\n{}\n'.format(str(key), str(var))
            output += '-' * 10 + '\n'
        return output

    def __init__(self, gender='0'):

        self.stay_info = StayInfo(gender)
        self.full_name = '{} {}'.format(self.stay_info.f_name, self.stay_info.l_name)
        self.room_number = self.stay_info.room_num

        self.use_minibar = True
        self.minibar_item_choice = ['water', 'coke']
        self.minibar_item_dict = {}

        self.payment = ["credit card", "cash"]

        self.clear_deposit = True
        self.left_item = ['passport', 'wallet']

        self.with_key = True

        # initialize
        self.random_init()

    def random_init(self):
        boolean = [True, False]

        if random.random() > 0.3:
            self.use_minibar = True
            minibar_items = random.randint(1, 3)
            self.minibar_item_dict = {
                random.choice(self.minibar_item_choice): random.randint(1, 4) for _ in range(minibar_items)}
        else:
            self.use_minibar = False

        self.payment = random.choice(self.payment)

        self.clear_deposit = random.choice(boolean)
        self.left_item = random.choice(self.left_item)

        self.with_key = random.choice(boolean)


if __name__ == '__main__':
    a = GuestInfo()
    print(a)
    a = vars(a.stay_info)
    print(a)

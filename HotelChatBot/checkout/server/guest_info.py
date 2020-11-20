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
        self.duration = 0
        self.folio_no = 'INV2189'
        self.room_num = '1618'
        self.r_rate = 400
        self.a_c_num = '1/0'
        self.cashier_id = 'LK'
        self.page = '1'

        self.print_date = self.d_date
        self.stay_2_date = ''
        self.stay_3_date = ''
        self.full_name = ''

        self.random_init()

    def random_init(self):

        if self.gender:  # if gender is male
            self.f_name = fake.first_name_male()
            self.l_name = fake.last_name_male()

        else:
            self.f_name = fake.first_name_female()
            self.l_name = fake.last_name_female()

        duration = random.randrange(1, 3)
        self.duration = duration
        self.a_date = self.d_date - datetime.timedelta(days=duration)
        self.stay_2_date = self.a_date + datetime.timedelta(days=1)
        self.stay_3_date = self.a_date + datetime.timedelta(days=2)
        self.a_date = self.a_date.strftime("%d-%b-%Y")
        self.d_date = self.d_date.strftime("%d-%b-%Y")
        self.stay_2_date = self.stay_2_date.strftime("%d %b %Y")
        self.stay_3_date = self.stay_3_date.strftime("%d %b %Y")
        self.folio_no = 'INV{}'.format(fake.random_int(0, 9999))

        self.room_num = '{}{}'.format(fake.random_int(1, 20), fake.random_int(10, 20))
        self.r_rate = random.randint(400, 700)
        self.a_c_num = '{}/{}'.format(fake.random_int(1, 2), fake.random_int(0, 4))
        self.cashier_id = fake.random_uppercase_letter() + fake.random_uppercase_letter()
        # self.page = random.randint(1, 10)
        self.print_date = self.d_date

        title = ['Mr', 'Ms'][self.gender]
        self.full_name = '{} {} {}'.format(title, self.f_name, self.l_name)

    def __str__(self):
        output = (
                'First Name: {}\t'.format(self.f_name) +
                'Last Name: {}\n'.format(self.l_name) +
                'Arrival Date: {}\n'.format(self.a_date) +
                'Departure Date: {}\n'.format(self.d_date) +
                'Folio No.: {}\n'.format(self.folio_no) +
                'Room No.: {}\t'.format(self.room_num) +
                'Room Rate.: {}\t'.format(self.r_rate) +
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
        self.minibar_item_choice = ['Coke Light', 'Coke', 'Pokka Tea', 'Evian Mineral Water', 'Perrier',
                                    'California Creamery Tortilla Chips', 'Tao Kae Noi Seaweed Snacks',
                                    'Cadbury Choc Bar', 'Ruffles Potato Chips']
        self.minibar_item_dict = {}
        self.minibar_item_add_qty_dict = {}

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
            samples = random.sample(self.minibar_item_choice, minibar_items)
            self.minibar_item_dict = {
                sample: random.randint(1, 10) for sample in samples}
            self.minibar_item_add_qty_dict = {
                "add_qty{}".format(self.minibar_item_choice.index(k)+1): str(v)
                for k, v in self.minibar_item_dict.items()
            }
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

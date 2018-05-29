# file to test out new code
# #########################


# customer/vertical adding/removing by storing a string, reading it out as list and store it back as string
# does not work, splits every character and places spaces between of every pre-existing name already in the db
# 'test'  -> 't e s t', it does not go beyond one space between each character
# m_customer = 'customer_' + version_x[8:]
# m_vertical = 'vertical_' + version_x[8:]
# customer_str = form.customer_str.data
# vertical_str = form.vertical_str.data
# customer_delete = form.customer_delete.data
# vertical_delete = form.vertical_delete.data
# customer_list = []
# vertical_list = []
#
# # fill customer_list, pass if no values
# try:
#     customers = getattr(module, m_customer)
#     for customer in customers:
#         customer_list.append(customer)
# except TypeError:
#     pass
# # fill vertical_list, pass if no values
# try:
#     verticals = getattr(module, m_vertical)
#     for vertical in verticals:
#         vertical_list.append(vertical.strip(' '))
# except TypeError:
#     pass
#
# # append to list, split input on spaces
# if customer_str != '':
#     for name in customer_str.split(' '):
#         customer_list.append(name)
# # append to list, split input on spaces
# if vertical_str != '':
#     for name in vertical_str.split(' '):
#         vertical_list.append(name)
#
# # delete items from customer_list
# if form.customer_delete.data != '':
#     for name in form.customer_delete.data.split(' '):
#         customer_list.remove(name)
# # delete items from vertical_list
# if form.vertical_delete.data != '':
#     for name in form.vertical_delete.data.split(' '):
#         vertical_list.remove(name)
#
# customers = ''
# verticals = ''
# # list back to string for storage
# customers = ' '.join(customer_list)
# verticals = ' '.join(vertical_list)
#
# setattr(module, m_customer, customers)
# setattr(module, m_vertical, verticals)

# file to test out new code
# #########################

from app.models import Module
from sqlalchemy import and_



def search_module_f(form_module_data,
                    form_select_version_data,
                    form_search_readme_data,
                    form_installable_bool_data, customer_data, vertical_data):
    version_x = 'version_' + form_select_version_data
    installable = 'installable_' + form_select_version_data
    readme_text = 'readme_text_' + version_x[8:]
    customer = 'customer_' + version_x[8:]
    vertical = 'vertical_' + version_x[8:]

    install_true = getattr(Module, installable) == 'True'
    install_false = getattr(Module, installable) == 'False'
    exists = getattr(Module, version_x) == 'X'
    like_module = Module.addon.like('%' + form_module_data + '%')
    like_readme = getattr(Module, readme_text).like('%' + form_module_data + '%')
    like_customer = getattr(Module, customer).like('%' + customer_data + '%')
    like_vertical = getattr(Module, vertical).like('%' + vertical_data + '%')




    if form_module_data != '':
        query = exists, like_module
        if form_search_readme_data is True:
            query = exists, like_module, like_readme
            if customer_data != '':
                query = exists, like_module, like_readme, like_customer
                if vertical_data != '':
                    query = exists, like_module, like_readme, like_customer, like_vertical
                    if form_installable_bool_data == 'True:':
                        query = exists, like_module, like_readme, like_customer, like_vertical, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_module, like_readme, like_customer, like_vertical, install_false
                    else:
                        query = exists, like_module, like_readme, like_customer, like_vertical  # could be a pass
                else:
                    if form_installable_bool_data == 'True:':
                        query = exists, like_module, like_readme, like_customer, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_module, like_readme, like_customer, install_false
                    else:
                        query = exists, like_module, like_readme, like_customer  # could be a pass
            elif vertical_data != '':
                query = exists, like_module, like_readme, like_vertical
                if form_installable_bool_data == 'True:':
                    query = exists, like_module, like_readme, like_vertical, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_module, like_readme, like_vertical, install_false
                else:
                    query = exists, like_module, like_readme, like_vertical  # could be a pass
            else:
                if form_installable_bool_data == 'True':
                    query = exists, like_module, like_readme, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_module, like_readme, install_false
                else:
                    query = exists, like_module, like_readme
        else:
            query = exists, like_module  # could be a pass
            if customer_data != '':
                query = exists, like_module, like_customer
                if vertical_data != '':
                    query = exists, like_module, like_customer, like_vertical
                    if form_installable_bool_data == 'True:':
                        query = exists, like_module, like_customer, like_vertical, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_module, like_customer, like_vertical, install_false
                    else:
                        query = exists, like_module, like_customer, like_vertical  # could be a pass
                else:
                    if form_installable_bool_data == 'True:':
                        query = exists, like_module, like_customer, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_module, like_customer, install_false
                    else:
                        query = exists, like_module, like_customer  # could be a pass
            elif vertical_data != '':
                query = exists, like_module, like_vertical
                if form_installable_bool_data == 'True:':
                    query = exists, like_module, like_vertical, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_module, like_vertical, install_false
                else:
                    query = exists, like_module, like_vertical  # could be a pass
            else:
                if form_installable_bool_data == 'True':
                    query = exists, like_module, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_module, install_false
                else:
                    query = exists, like_module
    else:
        query = exists
        if form_search_readme_data is True:
            query = exists, like_readme
            if customer_data != '':
                query = exists, like_readme, like_customer
                if vertical_data != '':
                    query = exists, like_readme, like_customer, like_vertical
                    if form_installable_bool_data == 'True:':
                        query = exists, like_readme, like_customer, like_vertical, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_readme, like_customer, like_vertical, install_false
                    else:
                        query = exists, like_readme, like_customer, like_vertical  # could be a pass
                else:
                    if form_installable_bool_data == 'True:':
                        query = exists, like_readme, like_customer, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_readme, like_customer, install_false
                    else:
                        query = exists, like_readme, like_customer  # could be a pass
            elif vertical_data != '':
                query = exists, like_readme, like_vertical
                if form_installable_bool_data == 'True:':
                    query = exists, like_readme, like_vertical, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_readme, like_vertical, install_false
                else:
                    query = exists, like_readme, like_vertical  # could be a pass
            else:
                if form_installable_bool_data == 'True':
                    query = exists, like_readme, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_readme, install_false
                else:
                    query = exists, like_readme
        else:
            query = exists
            if customer_data != '':
                query = exists, like_customer
                if vertical_data != '':
                    query = exists, like_customer, like_vertical
                    if form_installable_bool_data == 'True:':
                        query = exists, like_customer, like_vertical, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_customer, like_vertical, install_false
                    else:
                        query = exists, like_customer, like_vertical  # could be a pass
                else:
                    if form_installable_bool_data == 'True:':
                        query = exists, like_customer, install_true
                    elif form_installable_bool_data == 'False':
                        query = exists, like_customer, install_false
                    else:
                        query = exists, like_customer  # could be a pass
            elif vertical_data != '':
                query = exists, like_vertical
                if form_installable_bool_data == 'True:':
                    query = exists, like_vertical, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, like_vertical, install_false
                else:
                    query = exists, like_vertical  # could be a pass
            else:
                if form_installable_bool_data == 'True':
                    query = exists, install_true
                elif form_installable_bool_data == 'False':
                    query = exists, install_false
                else:
                    query = exists

    modules = Module.query.filter(and_(*query)).all()
    return modules


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

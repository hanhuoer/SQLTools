import re

result = '''
(root@localhost:mysql.sock) [zx_cloud_app]>select * from client where id = '1';
+--------+-------+-------+-------+-------+-------+--------+-------+-------+-------+-------+-------+-------+-------+---------------------+---------+-------+---------------------+
| id     | field | field | field | field | field | field  | field | field | field | field | field | field | field | field               | field   | field | field               |
+--------+-------+-------+-------+-------+-------+--------+-------+-------+-------+-------+-------+-------+-------+---------------------+---------+-------+---------------------+
| 1      | value | value | value | value | value | value  | value | value | value | value | value | value | value | 2019-06-27 10:08:27 | value   | value | 2019-06-27 10:08:27 |
+--------+-------+-------+-------+-------+-------+--------+-------+-------+-------+-------+-------+-------+-------+---------------------+---------+-------+---------------------+
1 rows in set (0.01 sec)
'''

sql = ''
table_name = ''
field_list = []
value_list = []

results = result.splitlines()


def get_table_name(content):
    return re.findall('from(.*?)where', content)[0]


def get_field_list(content):
    return re.findall('(\w+)', content)


def get_value_list(content):
    return re.findall('\|\s+([0-9]{4}-[0-9]{1,2}-[0-9]{1,2}\s?[0-9]{1,2}:[0-9]{2}:[0-9]{2}|!\s{2}|.*?|)\s{1}', content)


def parse_data():
    global table_name
    global field_list
    global value_list
    for index, item in enumerate(results):
        if index == 1:
            table_name = get_table_name(item)
        if index == 3:
            field_list = get_field_list(item)
        if index > 3:
            list.append(value_list, get_value_list(item))


def get_statement_table():
    return 'INSERT INFO #table_name '.replace('#table_name', table_name)


def get_statement_fields():
    fields = '('
    for f in field_list:
        fields += f + ', '
    fields = fields[:-2] + ')'
    return fields


def get_statement_values():
    statement_values = ' VALUES '
    for values in value_list:
        if len(values) == 0:
            continue
        statement_value = '('
        for value in values:
            if value != 'NULL' and value != 'null':
                statement_value += '\'' + value + '\'' + ', '
            else:
                statement_value += value + ', '
        statement_value = statement_value[:-2] + '), '
        statement_values += statement_value
    statement_values = statement_values[:-2]
    return statement_values


def get_sql():
    statement = ''
    statement += get_statement_table()
    statement += get_statement_fields()
    statement += get_statement_values()
    statement = statement.replace('  ', ' ')
    print(statement)


def main():
    parse_data()
    print('table_name: ' + table_name)
    print('field_list: ', field_list)
    print('value_list: ', value_list)
    get_sql()


if __name__ == '__main__':
    main()

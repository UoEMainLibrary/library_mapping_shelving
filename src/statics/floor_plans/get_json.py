import mysql.connector
import json

def output_json(output, library, floor):
    output_dict = {}
    output_dict[library+str(floor)] = []
    for c in output:
        output_dict[library+str(floor)].append(c)
    f = open(library+str(floor)+'.json', 'w')
    f.write(json.dumps(output_dict))
    f.close()
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    #passwd="Cr@n1eri",
    port='3306',
    charset='utf8'
)

cursor = mydb.cursor()
cursor.execute("USE LibraryMapping_production;")

libraries = []

cursor.execute("""SELECT DISTINCT library FROM elements WHERE library != 'None';""")
for x in cursor:
    libraries.append(x[0])

floor_and_library= {}
for library in libraries:
    floor_and_library[library] = []
    cursor.execute("""SELECT DISTINCT floor FROM elements WHERE library = '"""+library+"""'""")
    for floor in cursor:
        floor = floor[0]
        floor_and_library[library].append(str(floor))
for library in libraries:
    for floor in floor_and_library[library]:
        query = """SELECT JSON_OBJECT(
        'id',elements.id,
        'name', `name`,
        'svg_path', svg_path,
        'width', width,
        'height',height,
        'floor', `floor`,
        'library',library,
        'top', top,
        'left', `left`,
        'angle', angle,
        'fill', fill,
        'opacity', opacity,
        'scaleX', scaleX,
        'scaleY', scaleY,
        'range_end',range_end,
        'range_end_opt', range_end_opt,
        'range_end_letters', range_end_letters,
        'range_end_digits', range_end_digits,
        'range_start', range_start,
        'range_start_opt', range_start_opt,
        'range_start_letters', range_start_letters,
        'range_start_digits', range_start_digits)
        FROM elements
        JOIN element_types
        ON elements.element_type_id = element_types.id
        WHERE library = '"""+library+"""'
        AND name = 'Shelf'
        AND floor = """+floor+""";"""
        cursor.execute(query)
        output = []
        for c in cursor:
            item = []
            for i in c:
                item.append(str(i))
            output.append(item)
        output_json(output, library, floor)

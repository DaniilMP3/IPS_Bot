import json


async def write_in_json(day, message):
    with open('schedule.json', 'r', encoding='utf-8') as f:
        schedule_dict = json.load(f)

    schedule_dict[day] = {'message': message.text, 'entities': [{'type': _.type,
                                                                  'offset': _.offset,
                                                                  'length': _.length,
                                                                  'url': _.url} for _ in message.entities]}

    rows_counter = 1
    for row in iter(message.text.splitlines()):
        schedule_dict[day][str(rows_counter)] = {'text': row}
        rows_counter += 1
    rows_counter = 1

    for _ in message.entities:
        single_row_text = schedule_dict[day][str(rows_counter)]['text']
        schedule_dict[day][str(rows_counter)]['entities'] = {'type': _.type,
                                                             'offset': 0,
                                                             'length': len(single_row_text),
                                                             'url': _.url}
        rows_counter += 1

    with open('schedule.json', 'w', encoding='utf-8') as file:
        json.dump(schedule_dict, file)





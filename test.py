import json

def count():
    count = 5
    while(count > 0):
        main_data = []
        data = {
            "Address":[{
                "Street":"Main St",
                "State":"WY"
            }],
        }
        main_data.append(data)
        with open('data.json', 'w') as outfile:
            json.dump(main_data, outfile)
        count = count -1;
        print(count)


def make_random():
    i = 1;
    data= []
    while(i < 13):
        
        names = str(i)
        i+=1
        
        date = {
            'names':[{
                'name': names
            }]
        }
        data.append(date)
    with open('cringe.json','w') as f:
        json.dump(data,f)


if __name__ == "__main__":
    print("hello")
    make_random()
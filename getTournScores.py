import requests, bs4

for i in range(1,31):

    resp = requests.get('http://localhost:8000/golfer/'+str(i))
    

    if resp.status_code == 200:
        

        golfer = bs4.BeautifulSoup(resp.text, "html.parser")
        

        golfer_name = golfer.find('h2').text.strip() 
        print( "Golfer: {}".format(golfer_name))
        

        td_list = golfer.select ('td')

        for i in range(0,len(td_list), 2):
            tourn_name = td_list[i].getText().strip() 
            tourn_score = td_list[i+1].getText().strip()
            row = tourn_name.ljust(21) + " " + tourn_score 
            print(row)
        print("\n")


  







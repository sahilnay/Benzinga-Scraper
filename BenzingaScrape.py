import requests
from bs4 import BeautifulSoup
from benzinga import financial_data




def writer(elems):
  count = 0
  newFileName = "Benzinga.txt"
  with open(newFileName, 'w') as filehandle:
    for stock in elems:
      count += 1
      filehandle.write(f'{count}) {stock}\n')

def weighter(elems):
  weights = dict()
  weights["Maintains"] = 1
  weights["Reinstates"] = 1
  weights["Upgrades"] = 3
  weights["Initiates Coverage On"] = 1.5
  weights["Downgrades"] = .5
  weights["Strong Buy"] = 10
  weights["Buy"] = 8
  weights["Outperform"] = 6
  weights["Market Outperform"] = 5
  weights["Overweight"] = 4
  weights["Assumes"] = 1

  for elem in elems:
    movement = elem[1]
    action = elem[2]
    movementWeight = weights[movement]
    actionWeight = weights[action]
    totalWeight = actionWeight * movementWeight
    elem.append(int(totalWeight))

  elems.sort(key = lambda x:x[3])
  elems.reverse()
  writer(elems)

    
  



def priceFinder():
  with open("BenzingaData.html", "r") as f:
    contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')
    tbody = soup.find_all('tbody')
    td = soup.find_all('td')
    counter = 0
    prev = ""
    Full = []
    temp = []
    goods = ["Buy", "Outperform", "Overweight", "Strong Buy", "Market Outperform"]
    for text in td:
      # Ticker Name of stock (Ticker)
      if text.a != None:
        counter = 1
        temp.append(text.a.string)

      # Direction Stock is going in (Action)

      if counter == 4:
        temp.append(text.string)
        
      
      # Curr Status (To)
      if counter == 6:
        #print(text.string)
        if text.string in goods:
          temp.append(text.string)
          Full.append(temp)
          temp = []
        else:
          temp = []
        counter = 0
      if counter >= 1:
        counter += 1
      
    print(weighter(Full))
    


if __name__ == 'main': 
  priceFinder()

def extract(entry):
  import json
  import requests
  import pandas as pd
  import os
  from pathlib import Path

  # set up the request parameters
  params = {
    'api_key': 'FAF5AA7EEFDC4C9687895F7B866FC69C',
    'type': 'search',
    'amazon_domain': 'amazon.com',
    'search_term': entry,
    'exclude_sponsored': 'true',
    'max_page': '2'
  }

  # make the http GET request to Rainforest API
  api_result = requests.get('https://api.rainforestapi.com/request', params)

  # now i am formatting the json
  json_file = json.dumps(api_result.json(), indent=4)
  # print(type(json_file))
  # print(json_file)

  # now i am saving it
  desktop_path = Path(os.path.expanduser("~/Desktop"))
  json2 = f'{desktop_path}/{entry}.txt'
  # # Write the JSON data to a file
  with open (json2, 'w') as file:
    file.write(json_file)

  # now converting the json to dict
  global dict_file
  dict_file = json.loads(json_file)
  # print(type(dict_file))
  # print(dict_file)

  products = []

  # now taking all the info i need
  for i in dict_file["search_results"]:
    title = i["title"]
    if "recent_sales" in i:
      recent_sales = i["recent_sales"]
      sale_num, trash = recent_sales.split("+")
      if "K" in sale_num:
        sale_num = int(sale_num[:-1])*1000
      else:
        sale_num = int(sale_num)
    else:
      sale_num = 0
    image = i['image']
    try:
      rating = i["rating"]
    except:
      rating = 0
    try:
      ratings_total = i["ratings_total"]
    except:
      ratings_total = 0
    link = i["link"]
    try:
      prices = i['prices']
      if len(prices)>1:
        o_d_prices = []
        for i in prices:
          for j in i:
            if j == "value":
              o_d_prices.append(i["value"])
            else:
              continue
        discounted_price = o_d_prices[0]
        try:
          original_price = o_d_prices[1]
        except:
          original_price = discounted_price
      else:
        original_price = prices[0]["value"]
        discounted_price = prices[0]["value"]
    except:
      original_price = discounted_price = 1

    discount = original_price - discounted_price
    discount_percent = (discount+original_price)/original_price

    formula = ((rating*(ratings_total+sale_num))/discounted_price)*discount_percent

    item = [title,sale_num,image,rating,ratings_total,discounted_price,original_price,discount,discount_percent,link,formula]
    products.append(item)

  global df
  df = pd.DataFrame(products, columns=["Title","Recent_Sales","Image","Rating","Rating_Total","Discounted_Price","Original_Price","Discount","Discount_Percent","Link","Formula"])
  df = df.sort_values(by=['Formula'])
  df.to_csv(f'{desktop_path}/{entry}.csv')
  return df
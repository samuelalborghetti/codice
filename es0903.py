# realizza programma python che permette di realizzare in automatico una pagina html confrontando il valore attuale delleuro con dollaro sterlina nuwan yen
import json
import os,datetime,requests 
#https://open.er-api.com/v6/latest/EUR

x= requests.get("https://open.er-api.com/v6/latest/EUR")
monetap = json.loads(x.text)

fris = open("risultati.html", "w", encoding="utf-8")
fris.write("""<!DOCTYPE html><html lang="it"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Risultati</title>
    <style>
        .titolo{
            color:red;
            background-color: aquamarine;
            font-family: 'Verdana';
            font-weight: bold;
            font-size: 30px;
            padding:30px;
            text-align: center;
        }
        .risultati{
            background-color: beige;
            font-family: 'Courier New';
            font-size: 20px;
            padding: 20px;
        }
        .footer{
            color: #919191;
            background-color: #dcdcdc;
            text-align: center;
            padding-top: 10px;
            padding-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="titolo">
        Risultati dei conteggi
    </div>
    <div class="risultati">""")
fris.write(f"Il tasso di cambio attuale tra EUR e le altre monete è: <br><br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['EUR']} Euro <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['GBP']} Sterline Inglesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['CAD']} Dollari Canadesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['JPY']} Yen Giapponesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['AUD']} Dollari Australiani <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['CHF']} Franchi Svizzeri <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['CNY']} Yuan Cinesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['SEK']} Corone Svedesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['NZD']} Dollari Neozelandesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['ZAR']} Rand Sudafricani <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['JPY']} Yen Giapponesi <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['INR']} Rupie Indiane <br>")
fris.write(f"Oggi 1 EUR vale: {monetap['rates']['BRL']} Real Brasiliani <br>")

d = datetime.datetime.now()
fris.write(f"""</div><div class="footer">&copy; {d.strftime("%d-%m-%Y")} - 3Ai Dalmine
    </div>
</body>
</html>""")

fris.close()


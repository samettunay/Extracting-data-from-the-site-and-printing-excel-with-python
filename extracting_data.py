from bs4 import BeautifulSoup
import numpy as np
import requests
import xlsxwriter
import keyboard as key
import signal
import os
import gc


excel_name = "adresler"
workbook = xlsxwriter.Workbook(f'C:\\Users\\Samet Tunay\\Desktop\\{excel_name}.xlsx')
worksheet = workbook.add_worksheet()

links = np.load('C:\\Users\\Samet Tunay\\Desktop\\links.npy')
link_sayisi = int(links.size)
print("Linkler yüklendi. Link sayısı: ", links.size)


 
def handler(signum, frame):
        workbook.close()
        exit(1)
 
signal.signal(signal.SIGINT, handler)
        
def get_data():
    x = 0
    row = 1
    column = 0
    global link_sayisi, links

    while x < link_sayisi:
        try:
            sayfa_url = links[x]

            try:
                response = requests.get(sayfa_url, timeout=5)
            except:
                link_sayisi += 1
                print(x + 1, ". adım tekrarlanıyor.")
                continue
            soup = BeautifulSoup(response.content, 'html.parser')

            

            # Başlık
            try:
                title = soup.select("h1.job_listing-title")
                title = str(title[0].getText())
                title = title.strip()
            except:
                print(x + 1, ". adım Title yok!")
                x += 1
                continue
            

            # Kategori
            try:
                kategori = soup.select("div.content-single-job_listing-title-category")[0]
                kategori_text = kategori.find_all("a")
                kategori_text = str(kategori_text[1].getText())
                kategori_text = kategori_text.strip()
            except:
                kategori_text = ""
            

            # Bölge
            try:
                il = soup.select("div.content-single-job_listing-title-category")[1]
                il = il.find('a')
                il = str(il.getText())
                il = il.strip()
            except:
                il = ""

            # İlçe
            toplam = ""
            try:
                ilce = soup.select("div.content-single-job_listing-title-category")[1]
                ilce = ilce.find_all('a')
                ilce = str(ilce[1].getText())
                ilce = ilce.strip()
            except:
                ilce = ""
            
            toplam = ilce
            try:
                ilce2 = soup.select("div.content-single-job_listing-title-category")[1]
                ilce2 = ilce2.find_all('a')
                ilce2 = str(ilce2[2].getText())
                ilce2 = ilce2.strip()
                toplam = ilce + " > " + ilce2
            except:
                pass
            
            
            # print("Bölge eklendi.")

            yemekli_fiyat = ""
            yemeksiz_fiyat = ""
            kokteyl_fiyat = ""
            havuz_alan = ""
            oto_alan = ""
            kapali_davet_alani = ""
            acik_alan = ""
            kir_alan = ""
            baslangic_paketi = ""
            her_sey_dahil = ""

            card_texts = soup.find_all("div", class_ = "card-outer")
            for i in range(0, 20):
                try:
                    card_text = str(card_texts[i].getText())
                    card_text = card_text.replace("\n", "")
                    card_text = card_text.split()

                    if card_text[0] == "Yemekli":
                        yemekli_fiyat = "Hafta içi: " + card_text[2] + ", " + "Hafta Sonu: " + card_text[6]

                    if card_text[0] == "Yemeksiz":
                        yemeksiz_fiyat = "Hafta içi: " + card_text[2] + ", " + "Hafta Sonu: " + card_text[6]

                    if card_text[0] == "Kokteyl":
                        kokteyl_fiyat = "Hafta içi: " + card_text[2] + ", " + "Hafta Sonu: " + card_text[6]
                        
                    if card_text[0] == "Kapalı":
                        kapali_davet_alani = "Min: " + card_text[3] + ", " + "Max: " + card_text[5]
                        
                    if card_text[0] == "Açık":
                        acik_alan = "Min: " + card_text[3] + ", " + "Max: " + card_text[5]
                        
                    if card_text[0] == "Kır":
                        kir_alan = "Min: " + card_text[3] + ", " + "Max: " + card_text[5]
                    
                    if card_text[0] == "Havuz":
                        havuz_alan = "Min: " + card_text[4] + ", " + "Max: " + card_text[6]

                    if card_text[0] == "Otopark":
                        oto_alan = card_text[1]

                    if card_text[0] == "Başlangıç":
                        baslangic_paketi = card_text[2]

                    if card_text[0] == "Her":
                        her_sey_dahil = card_text[4]                                      
                except:
                    pass
            
            # Mekan Özellikleri
            toplam_mekan_ozelligi = ""
            for i in range(1, 30):
                try:
                    mekan_ozellikleri = soup.select("ul.space-features-list")[0]
                    mekan_ozellikleri = mekan_ozellikleri.find_all("li")
                    mekan_ozellikleri = str(mekan_ozellikleri[i].getText())
                    mekan_ozellikleri = mekan_ozellikleri.strip()
                    toplam_mekan_ozelligi = toplam_mekan_ozelligi + ", " + mekan_ozellikleri
                    toplam_mekan_ozelligi = toplam_mekan_ozelligi.lstrip(", ")
                except:
                    pass

            # Hakkında
            try:
                hakkinda = soup.find("div", class_ = "description-area")
                hakkinda = str(hakkinda.getText())
                hakkinda = hakkinda.strip()
            except:
                hakkinda = ""

            # Sorular
            soru_ve_cevap = ""
            for i in range(1, 15):
                try:
                    sorgu = soup.select(f"#questions > div:nth-child(2) > div > div:nth-child({i})")[0]
                    soru = sorgu.find("h6")
                    cevap = sorgu.find("p")
                    soru = str(soru.getText())
                    soru = soru.strip()
                    cevap = str(cevap.getText())
                    cevap = cevap.strip()
                    soru_ve_cevap = soru_ve_cevap + soru + "\n" + cevap + "\n"
                except:
                    pass
            
            try:
                phone = soup.select("a.job_listing-phone.button.button-phone")[0].getText()
            except:
                phone = ""
            
            
            worksheet.write(row, column, sayfa_url)
            column += 1
            worksheet.write(row, column, title)
            column += 1
            worksheet.write(row, column, kategori_text)
            column += 1
            worksheet.write(row, column, il)
            column += 1
            worksheet.write(row, column, toplam)
            column += 1
            worksheet.write(row, column, phone)
            column += 1
            worksheet.write(row, column, yemekli_fiyat)
            column += 1
            worksheet.write(row, column, yemeksiz_fiyat)
            column += 1
            worksheet.write(row, column, kokteyl_fiyat)
            column += 1
            worksheet.write(row, column, kapali_davet_alani)
            column += 1
            worksheet.write(row, column, acik_alan)
            column += 1
            worksheet.write(row, column, kir_alan)
            column += 1
            worksheet.write(row, column, havuz_alan)
            column += 1
            worksheet.write(row, column, oto_alan)
            column += 1
            worksheet.write(row, column, baslangic_paketi)
            column += 1
            worksheet.write(row, column, her_sey_dahil)
            column += 1
            worksheet.write(row, column, toplam_mekan_ozelligi)
            column += 1
            worksheet.write(row, column, hakkinda)
            column += 1
            worksheet.write(row, column, soru_ve_cevap)
            column += 1

            row += 1
            column = 0
            print(str(x + 1) + ". Sayfadan veriler çekildi")
            x += 1
            try:
                del title, yemekli_fiyat, yemeksiz_fiyat, kokteyl_fiyat, havuz_alan, oto_alan, kapali_davet_alani, acik_alan, kir_alan, ilce, toplam, soru, cevap, soru_ve_cevap, mekan_ozellikleri, toplam_mekan_ozelligi, hakkinda, card_text, card_texts, kategori
                gc.collect()
            except:
                pass
        except:
            print("Error!")
            workbook.close()
            x += 1
            pass
        

def basliklari_olustur():
    row = 0
    column = 0
    worksheet.write(row, column, "Link")
    column += 1
    worksheet.write(row, column, "Başlık")
    column += 1
    worksheet.write(row, column, "Kategori")
    column += 1
    worksheet.write(row, column, "İl")
    column += 1
    worksheet.write(row, column, "İlçe")
    column += 1
    worksheet.write(row, column, "Telefon")
    column += 1
    worksheet.write(row, column, "Yemekli Fiyat")
    column += 1
    worksheet.write(row, column, "Yemeksiz Fiyat")
    column += 1
    worksheet.write(row, column, "Kokteyl Fiyat")
    column += 1
    worksheet.write(row, column, "Kapalı Davet Alanı")
    column += 1
    worksheet.write(row, column, "Açık Davet Alanı")
    column += 1
    worksheet.write(row, column, "Kır Bahçesi Alanı")
    column += 1
    worksheet.write(row, column, "Havuz Başı Davet Alanı")
    column += 1
    worksheet.write(row, column, "Otopark Alanı")
    column += 1
    worksheet.write(row, column, "Başlangıç Paketi")
    column += 1
    worksheet.write(row, column, "Her Şey Dahil Paket")
    column += 1
    worksheet.write(row, column, "Mekan Özellikleri")
    column += 1
    worksheet.write(row, column, "Hakkında")
    column += 1
    worksheet.write(row, column, "Sorular")
    column += 1


basliklari_olustur()
get_data()
workbook.close()

    





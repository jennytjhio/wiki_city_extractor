import scrapy


class PapuaWikiSpider(scrapy.Spider):
    name = "papua_wiki"
    allowed_domains = ["en.wikipedia.org"]

    papua_cities = [
        "MAYBRAT",
        "SORONG",
        "MERAUKE",
        "JAYAWIJAYA",
        "NABIRE",
        "PANIAI",
        "PUNCAK JAYA",
        "MIMIKA",
        "BOVEN DIGOEL",
        "MAPPI",
        "ASMAT",
        "YAHUKIMO",
        "BINTANG MOUNTAINS",
        "TOLIKARA",
        "NDUGA",
        "LANNY JAYA",
        "CENTRAL MAMBERAMO",
        "YALIMO",
        "PUNCAK",
        "DOGIYAI",
        "INTAN JAYA",
        "DEIYAI"
    ]

    start_urls = ["https://en.wikipedia.org/wiki/" + "_".join((city.title().split(" ") + ['Regency'])) for city in papua_cities]

    def find_capital(self, response):
        capital_terms = ["Capital", "Regency seat", "Seat"]
        for term in capital_terms:
            capital = response.xpath("//th/a[contains(text(), '" + term + "')]/../../td//text()").get()
            if capital:
                return capital

    def parse(self, response):
        luas_wilayah = response.xpath("//th[contains(text(), 'Area')][@colspan=2]/../following-sibling::tr[1]/td/text()").get()
        luas_wilayah_wo_km = luas_wilayah.replace("km", "").strip()
        penduduk = response.xpath("//th[contains(text(), 'Population')][@colspan=2]/../following-sibling::tr[1]/td/text()").get()
        density = response.xpath("//th[contains(text(), 'Population')][@colspan=2]/../following-sibling::tr[2]/td/text()").get()
        ibu_kabupaten = self.find_capital(response)
        jumlah_kecamatan = (len(response.xpath('//table[contains(.//th/text(), "Kode")]//tr')) or len(response.xpath('//table[contains(.//th/text(), "Code")]//tr'))) - 2

        yield {
            "city": response.css(".mw-page-title-main::text").get(),
            "luas_wilayah": luas_wilayah_wo_km,
            "penduduk": penduduk,
            "density": density,
            "ibu_kabupaten": ibu_kabupaten,
            "jumlah_kecamatan": jumlah_kecamatan,
        }

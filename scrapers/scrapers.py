from scrapers.scraper import Scraper
from typing import Dict
from scrapers.hib_scraper import HibScraper
from scrapers.nkr_scraper import NkrScraper
from scrapers.bfdi_scraper import BfdiScraper
from scrapers.bva_scraper import BvaScraper
from scrapers.dsc_scraper import DscScraper
from scrapers.bsi_scraper import BsiScraper
from scrapers.bna_scraper import BnaScraper
from scrapers.diw_scraper import DiwScraper
from scrapers.bmds_scraper import BmdsScraper
from scrapers.bmi_scraper import BmiScraper
from scrapers.bmwe_scraper import BmweScraper
from scrapers.bmas_scraper import BmasScraper
from scrapers.breg_scraper import BregScraper
from scrapers.bmf_scraper import BmfScraper
from scrapers.bmbfsfj_scraper import BmbfsfjScraper
from scrapers.bmjv_scraper import BmjvScraper
from scrapers.bmftr_scraper import BmftrScraper
from scrapers.bmv_scraper import BmvScraper
from scrapers.bmukn_scraper import BmuknScraper
from scrapers.google_scraper import GoogleScraper
from scrapers.bmvg_scraper import BmvgScraper
from scrapers.bmg_scraper import BmgScraper
from scrapers.bmleh_scraper import BmlehScraper
from scrapers.bmz_scraper import BmzScraper
from scrapers.bmwsb_scraper import BmwsbScraper
from scrapers.aa_scraper import AaScraper

ALL_SCRAPERS: Dict[str, Scraper] = {
    "Heute im Bundestag": HibScraper(),
    "Normenkontrollrat": NkrScraper(),
    "BfDI": BfdiScraper(),
    "BVA": BvaScraper(),
    "DSC": DscScraper(),
    "BSI": BsiScraper(),
    "BNA": BnaScraper(),
    "DIW": DiwScraper(),
    "BMDS": BmdsScraper(),
    "BMI": BmiScraper(),
    "BMWE": BmweScraper(),
    "BMAS": BmasScraper(),
    "BREG": BregScraper(),
    "BMF": BmfScraper(),
    "BMBFSFJ" :BmbfsfjScraper(),
    "BMJV" : BmjvScraper(),
    "BMFTR": BmftrScraper(),
    "BMV" : BmvScraper(),
    "BMUKN":BmuknScraper(),
    "Google News":GoogleScraper(),
    "BMVG":BmvgScraper(),
    "BMG":BmgScraper(),
    "BMLEH":BmlehScraper(),
    "BMZ":BmzScraper(),
    "BMWSB":BmwsbScraper(),
    "AA":AaScraper(),
}

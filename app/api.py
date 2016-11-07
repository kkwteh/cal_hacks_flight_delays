import os

from flask import Blueprint, request, jsonify

from math import exp
bp = Blueprint('app', __name__)

MODEL_COEFFICIENTS = {
 'CarrierAA': -0.0019204985425103213,
 'CarrierAS': -0.84841944514035605,
 'CarrierB6': 0.12241821143901417,
 'CarrierDL': -0.13261989508615579,
 'CarrierEV': -0.010973177444743456,
 'CarrierF9': 0.0,
 'CarrierHA': 0.0,
 'CarrierNK': 0.0,
 'CarrierOO': -0.023123225427465505,
 'CarrierUA': 0.16964701242785432,
 'CarrierVX': -0.053647076481738616,
 'CarrierWN': -0.10363757129666461,
 'DayOfWeek1': 0.063727159827779406,
 'DayOfWeek2': -0.1853191855446592,
 'DayOfWeek3': -0.30014428231028273,
 'DayOfWeek4': -0.094916176670324648,
 'DayOfWeek5': -0.062572400878981818,
 'DayOfWeek6': -0.084710367475524101,
 'DayOfWeek7': -0.21834041248771782,
 'DepTimeBucket0': 1.3627774299145421,
 'DepTimeBucket1': -1.9928496577654837,
 'DepTimeBucket2': -0.82127521506520362,
 'DepTimeBucket3': -0.27652436329447116,
 'DepTimeBucket4': 0.17856868964922734,
 'DepTimeBucket5': 0.66702745101136107,
 'OriginGroup0': -0.67761214167229855,
 'OriginGroup1': -0.25382448266698804,
 'OriginGroup2': -0.11041084237121421,
 'OriginGroup3': -0.067072611283875219,
 'OriginGroup4': 0.22664441244453568}
MODEL_INTERCEPT = -0.88227567

ORIGIN_GROUPS = [{'ABR',  'ADQ',  'AMA',  'ANC',  'ATW',  'AZO',  'BET',  'BFL',  'BIL',  'BIS',  'BRW',  'BTM',  'BZN',  'CDC',  'CIU',  'CPR',  'DLG',  'DVL',  'EFD',  'EKO',  'EWN',  'FCA',  'FNT',  'FSD',  'GCC',  'GEG',  'GFK',  'GJT',  'GTF',  'HDN',  'HLN',  'HNL',  'HRL',  'HYS',  'IDA',  'INL',  'ISN',  'ITH',  'ITO',  'JMS',  'JNU',  'KOA',  'KTN',  'LCH',  'LIH',  'LSE',  'LWS',  'MOT',  'MQT',  'MSO',  'OGG',  'PIH',  'PLN',  'PPG',  'RKS',  'SCC',  'SGU',  'SIT',  'TWF',  'WYS',  'YUM'},
{'ABY',  'ASE',  'BDL',  'BGM',  'BMI',  'BOI',  'BQK',  'BRD',  'BRO',  'BUF',  'CHA',  'COD',  'CRP',  'CWA',  'DAY',  'DSM',  'ECP',  'EGE',  'ERI',  'EUG',  'EYW',  'FAR',  'FWA',  'GNV',  'GRB',  'GRK',  'GRR',  'GST',  'GUC',  'ILM',  'JAC',  'LAN',  'LAR',  'LBB',  'LNK',  'MAF',  'MCI',  'MHT',  'MKE',  'MLB',  'MRY',  'MTJ',  'OKC',  'OMA',  'OTZ',  'PDX',  'PHF',  'PIT',  'PSC',  'PSE',  'RHI',  'ROW',  'RST',  'SBP',  'SDF',  'SGF',  'SJC',  'SLC',  'TLH',  'TUL',  'XNA'},
{'ABQ',  'AKN',  'ALB',  'APN',  'AVP',  'BHM',  'BJI',  'BUR',  'CAK',  'CMH',  'DCA',  'DRO',  'ELP',  'FAI',  'FAT',  'FLG',  'FSM',  'GPT',  'GSP',  'HIB',  'HSV',  'IAD',  'ICT',  'IMT',  'IND',  'ISP',  'JAN',  'JAX',  'LGB',  'LIT',  'MBS',  'MEM',  'MLU',  'MSN',  'MSY',  'OAK',  'OME',  'ONT',  'PAH',  'PIA',  'PNS',  'PSG',  'PVD',  'PWM',  'RAP',  'RNO',  'ROC',  'RSW',  'SAN',  'SAT',  'SEA',  'SMF',  'SNA',  'SPS',  'STT',  'SYR',  'TRI',  'TUS',  'TXK',  'UST',  'VLD'},
{'ACK',  'ATL',  'AUS',  'BNA',  'BOS',  'BTR',  'BWI',  'CAE',  'CHS',  'CID',  'CLE',  'CLL',  'CMX',  'COS',  'CRW',  'CSG',  'CVG',  'DAB',  'DTW',  'EVV',  'FAY',  'GCK',  'GSO',  'GTR',  'HOB',  'HOU',  'HYA',  'IAH',  'LEX',  'LFT',  'LRD',  'MDW',  'MFE',  'MFR',  'MGM',  'MLI',  'MOB',  'MSP',  'OAJ',  'ORF',  'PBI',  'PHL',  'PHX',  'PIB',  'PSP',  'RDU',  'RIC',  'ROA',  'SBA',  'SBN',  'SHV',  'STL',  'STX',  'SUN',  'TPA',  'TTN',  'TVC',  'TYS',  'VPS',  'WRG',  'YAK'},
{'ABE',  'ABI',  'ACT',  'ACV',  'ACY',  'ADK',  'AEX',  'AGS',  'AVL',  'BGR',  'BPT',  'BQN',  'BTV',  'CDV',  'CHO',  'CLT',  'DAL',  'DEN',  'DFW',  'DHN',  'DLH',  'EAU',  'ELM',  'ESC',  'EWR',  'FLL',  'GGG',  'GRI',  'GUM',  'HPN',  'IAG',  'JFK',  'JLN',  'LAS',  'LAW',  'LAX',  'LBE',  'LGA',  'MCO',  'MDT',  'MEI',  'MIA',  'MKG',  'MVY',  'MYR',  'ORD',  'ORH',  'OTH',  'PBG',  'RDD',  'RDM',  'SAF',  'SAV',  'SCE',  'SFO',  'SJT',  'SJU',  'SMX',  'SPI',  'SRQ',  'SWF'}]

DEP_TIME_THRESHOLDS = [400, 800, 1200, 1600, 2000, 2400]

@bp.route('/')
def hello():
    return 'hello world'


@bp.route('/flight_delay_prediction', methods=['POST', 'OPTIONS'])
def flight_delay_prediction():
    payload = request.get_json(force=True)
    return jsonify({'prediction': prediction(payload['data'])})

def prediction(data):
    operand = MODEL_INTERCEPT

    operand += MODEL_COEFFICIENTS['Carrier%s' % data['carrier']]
    operand += MODEL_COEFFICIENTS['DayOfWeek%s' % data['day_of_week']]

    for i, threshold in enumerate(DEP_TIME_THRESHOLDS):
        if int(data['departure_time']) < threshold:
            time_bucket = i
            operand += MODEL_COEFFICIENTS['DepTimeBucket%s' %i]
            break

    for i, origin_group in enumerate(ORIGIN_GROUPS):
        if data['origin'] in origin_group:
            group_number = i
            operand += MODEL_COEFFICIENTS['OriginGroup%s' %group_number]
            break

    return 1 / (1 + exp(-1 * operand))

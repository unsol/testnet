import argparse, json, sys, binascii

parser = argparse.ArgumentParser(description='Preload a Geth genesis with contract accounts')
parser.add_argument('--genesis', type=str, nargs='?',
                            help='path to the genesis source template')
parser.add_argument('--preload', type=str, nargs='?',
                            help='a json object of the form \'{ address1:  { codefile: "/path/to/file/containing/accountcode", code: "accountcode", balance: ""}, ... }\'.  \'code\' and \'codefile\ are mutually exclusive')

parse_args = parser.parse_args()

genesis = parse_args.genesis
preload = parse_args.preload

try:
  with open(genesis) as f:
    genesis = json.load(f)
except Exception as e:
  print(e)
  sys.exit(1)

preload = json.loads(preload)
for address in preload.keys():
  acct = preload[address]

  if not 'balance' in acct:
    acct['balance'] = 0

  if 'codefile' in acct:
    try:
      with open(acct['codefile'], 'rb') as f:
        acct['code'] = binascii.hexlify(f.read())
    except Exception as e:
      print(e)
      sys.exit(1)
  elif not 'code' in acct:
    acct['code'] = ''
    
  genesis['alloc'][address] = json.dumps({
    'code': '0x'+acct['code'],
    'balance': acct['balance']
  })

print(genesis)

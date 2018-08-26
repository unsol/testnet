import argparse, json, sys, binascii

parser = argparse.ArgumentParser(description='Preload a Geth genesis with contract accounts')
parser.add_argument('precompiles', type=str, nargs='+',
                            help='one or more json objects of the form {address: "" , codefile: "/path/to/file/containing/accountcode", code: "accountcode", balance: ""}')
parser.add_argument('--genesis', metavar='g', type=str, nargs='?',
                            help='a string of the form address,codefile')

genesis = None

args = parser.parse_args()

try:
  with open('genesis.json') as f:
    genesis = json.load(f)
except Exception as e:
  print(e)
  sys.exit(1)

for arg in args.precompiles:
  acct = json.loads(arg)

  if not 'address' in acct:
    raise Exception("account must have an address")

  if not 'balance' in acct:
    acct['balance'] = 0

  if 'codefile' in acct:
    try:
      with open(codefile, 'rb') as f:
        acct['code'] = binascii.hexlify(f.read())
    except Exception as e:
      print(e)
      sys.exit(1)
  elif not 'code' in acct:
    acct['code'] = ''
    
  genesis['alloc'][acct['address']] = json.dumps({
    'code': acct['code'],
    'balance': acct['balance']
  })

print(genesis)

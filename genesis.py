import argparse, json, sys, binascii

parser = argparse.ArgumentParser(description='Preload a Geth genesis with contract accounts')
parser.add_argument('precompiles', type=str, nargs='+',
                            help='a string of the form address,codefile')
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
  if len(args.split(",")) != 2:
    raise Exception("invalid argument for precompiles {0}".format(args))

  address = arg.split(",")[0] #TODO validation
  codefile = arg.split(",")[1]

  try:
    with open(codefile, 'rb') as f:
      genesis['alloc'][address] = binascii.hexlify(f.read())
  except Exception as e:
    print(e)
    sys.exit(1)

print genesis

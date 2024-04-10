from collections import defaultdict
from math import lcm

class Day20:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

  def p1(self):
    
    moduleDestinations = defaultdict(list)

    incomingModules = defaultdict(list)

    nameToIndex = {}

    conjunctionIndex = 48
    flipflopIndex = 0

    for line in self.input:
      
      name, destinationString = line.split(" -> ")

      isConjunctionModule = name[0] == '&'
      isFlipFlopModule = name[0] == '%'

      destinations = destinationString.split(", ")

      if name == 'broadcaster':
        broadcaster = destinations
        continue

      name = name[1:]

      if name not in nameToIndex:
        if isConjunctionModule:
          nameToIndex[name] = conjunctionIndex
          conjunctionIndex += 1
        elif isFlipFlopModule:
          nameToIndex[name] = flipflopIndex
          flipflopIndex += 1

      for dst in destinations:
        if dst == 'rx':
          continue
        incomingModules[dst].append(name)
      
      moduleDestinations[name].extend(destinations)

    incoming = [[] for _ in range(9)]
    outgoing = [[] for _ in range(57)]

    for module, destinations in moduleDestinations.items():

      for destination in destinations:

        if destination == 'rx':
          outgoing[nameToIndex[module]].append(57)
        else:
          outgoing[nameToIndex[module]].append(nameToIndex[destination])

    for dst, sources in incomingModules.items():
      
      dstIndex = nameToIndex[dst]

      if dstIndex < 48:
        continue
      
      dstIndex -= 48

      for source in sources:
        incoming[dstIndex].append(nameToIndex[source])

    buttonPushes = 1000

    lowPulses = highPulses = 0

    state = 0

    for _ in range(buttonPushes):

      q = [nameToIndex[dest] for dest in broadcaster]

      lowPulses += len(broadcaster)

      i = 0

      while i < len(q):

        moduleIndex = q[i]

        if moduleIndex == 57:
          i += 1
          continue

        if moduleIndex < 48:

          state ^= 1 << moduleIndex

        else:

          if all([state & 1 << srcIndex for srcIndex in incoming[moduleIndex - 48]]):

            state &= ~(1 << moduleIndex)

          else:

            state |= 1 << moduleIndex

        hi = state & 1 << moduleIndex

        if hi:
          highPulses += len(outgoing[moduleIndex])
        else:
          lowPulses += len(outgoing[moduleIndex])

        for dest in outgoing[moduleIndex]:

          if dest < 48 and hi:
            continue

          q.append(dest)
        
        i += 1

    print('p1', (buttonPushes + lowPulses) * highPulses)

  def p2(self):
    
    moduleDestinations = defaultdict(list)

    incomingModules = defaultdict(list)

    nameToIndex = {}
    conjunctionIndex = 48
    flipflopIndex = 0

    indexToName = [None] * 57 + ['rx']

    for line in self.input:
      
      name, destinationString = line.split(" -> ")

      isConjunctionModule = name[0] == '&'
      isFlipFlopModule = name[0] == '%'

      destinations = destinationString.split(", ")

      if name == 'broadcaster':
        broadcaster = destinations
        continue

      name = name[1:]

      if name not in nameToIndex:
        if isConjunctionModule:
          nameToIndex[name] = conjunctionIndex
          indexToName[conjunctionIndex] = name
          conjunctionIndex += 1
        elif isFlipFlopModule:
          nameToIndex[name] = flipflopIndex
          indexToName[flipflopIndex] = name
          flipflopIndex += 1

      for dst in destinations:
        if dst == 'rx':
          continue
        incomingModules[dst].append(name)
      
      moduleDestinations[name].extend(destinations)

    incoming = [[] for _ in range(9)] # list of incoming modules for conjunctions only identified by index - 48
    outgoing = [[] for _ in range(57)] # destinations for all modules

    for module, destinations in moduleDestinations.items():

      for destination in destinations:

        if destination == 'rx':
          outgoing[nameToIndex[module]].append(57)
        else:
          outgoing[nameToIndex[module]].append(nameToIndex[destination])

    for dst, sources in incomingModules.items():
      
      dstIndex = nameToIndex[dst]

      if dstIndex < 48:
        continue
      
      dstIndex -= 48

      for source in sources:
        incoming[dstIndex].append(nameToIndex[source])

    buttonPushes = 0

    globalConjunctionSendingLowPulse = set()

    state = 0

    while buttonPushes < 10000:

      buttonPushes += 1

      q = [nameToIndex[dest] for dest in broadcaster]

      rxLowPulsesReceived = rxHiPulsesReceived = 0

      conjunctionSendingLowPulse = set()

      # print([indexToName[i] for i in q])

      while q:

        nextLevel = []
        
        for moduleIndex in q:

          if moduleIndex == 57: # rx no outgoing
            continue

          if moduleIndex < 48: # flipflop
            
            state ^= 1 << moduleIndex

          else: # conjunction

            if all([state & 1 << srcIndex for srcIndex in incoming[moduleIndex - 48]]): # receiving all hi
              
              if indexToName[moduleIndex] in conjunctionSendingLowPulse:
                print("found")
                # This never executed meaning that the graph is relatively simple (no nasty cycles)
                # I guess this could also have been inferred from the queue being able to empty at all (finite propagation)

              if len(incoming[moduleIndex - 48]) > 1:
                conjunctionSendingLowPulse.add(indexToName[moduleIndex])

              state &= ~(1 << moduleIndex)

            else: # receiving not all hi from inputs

              state |= 1 << moduleIndex

          hi = state & 1 << moduleIndex

          for dest in outgoing[moduleIndex]:

            if dest < 48 and hi:
              continue
            
            if dest == 57:
              if hi:
                rxHiPulsesReceived += 1
              else:
                rxLowPulsesReceived += 1
              continue

            nextLevel.append(dest)

        # print([('%' if index < 48 else '&', indexToName[index]) for index in q])

        q = nextLevel

        if rxLowPulsesReceived > 0:
          print('p2', buttonPushes)
          return

      if len(conjunctionSendingLowPulse) > 0:
        print(buttonPushes, conjunctionSendingLowPulse)

      # if len(conjunctionSendingLowPulse) > 0:
      #   for name in conjunctionSendingLowPulse:
      #     if name not in globalConjunctionSendingLowPulse:
      #       print(buttonPushes, name)
      #       globalConjunctionSendingLowPulse.add(name)
    
    # Found by trial and error that conjunctions sending low pulses repeat every N buttonPushes

    # buttonPushes to send a low pulse for each conjunction:
    # 4093 fd
    # 4021 kb
    # 3797 mf
    # 3907 nh

    # Studying the input: for rx to receive lo from inverter kc, all of: (kt hn vn ph) must receive a single hi for the span of that button push

    # kc is rx's only input
    
    # kt hn vn ph are all inverters

    # when fd send lo, kt send hi to kc

    # when kb send lo, hn send hi to kc

    # when mf send lo, vn send hi to kc

    # when nh send lo, ph send hi to kc

    # Take the lowest common multiple of buttonPushes that send low pulses for fd, kb, mf, nh

    print("p2", lcm(3797, 3907, 4021, 4093))

d20 = Day20()
d20.p1()
d20.p2()

# don't transmit lows to flipflops

# optimise or simulate in another way

# all next state dependent on prev state

# concept of time
# input analysis
# single input/ouput or single input modules?
# path compression?
# high pulses only relevant when conjunction -> conjunction
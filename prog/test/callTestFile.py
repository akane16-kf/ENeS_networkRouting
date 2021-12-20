from parsingXML import ParsingXML as PXML

PXML = PXML('sumoTrace.txt')
dict = PXML.main()

print(dict)

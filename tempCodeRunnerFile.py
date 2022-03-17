"./parsed_forms/op_10q.txt", "w")
for match in txt:
    print(match)
    op.write(match.group())

op.close()
exit()
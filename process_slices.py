slices = [1, 6, 12, 36, 60, 90, 119, 138, 154, 172, 227, 242, 263, 282, 307, 344, 398, 469, 508, 525, 552, 578, 622, 669, 711, 740, 795, 848, 862, 919, 973, 1006, 1050, 1086, 1177, 1238, 1318, 1379, 1420, 1457, 1496, 1560, 1630, 1680, 1758, 1796, 1864, 1910, 1951, 1998, 2056, 2109, 2188, 2225, 2266, 2335]

SHORTEST = 100

def ensure_length(slices: list[int], shortest=SHORTEST):
	start = 0
	while (start < len(slices) - 1):
		end = start + 1
		while (end < len(slices) and (slices[end] - slices[start]) < shortest):
			end += 1
		del slices[start + 1:end]
		start += 1

	if (len(slices) > 1 and (slices[-1] - slices[-2]) < shortest):
		del slices[-1]

	return slices

def ensure_end_on_period(words: list[str], slices: list[int]):
	# starting from the second slices, ensure that each slice ends on a period
	# start at that index then search left and right for the nearest period

	for i in range(1, len(slices)):
		end = slices[i]
		if (words[end - 1][-1] != '.'):
			# search left and right for nearest period
			left = end - 1
			right = end
			while (left > slices[i - 1] and right < len(words)):
				if (words[left][-1] == '.'):
					slices[i] = left + 1
					break
				elif (words[right][-1] == '.'):
					slices[i] = right + 1
					break
				left -= 1
				right += 1

	return slices

def ensure_start_at_beginning(slices):
	slices[0] = 0
	return slices

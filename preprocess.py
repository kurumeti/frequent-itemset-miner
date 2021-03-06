import re

class Preprocess:
	__instance = None
	_patterns = {
		"MIS":r"MIS\(([\w-]+)\)\s*[\=\:]\s*([\d.]+)",
		"others":r"(others)\s*[\=\:]\s*([\d.]+)",
		"SDC":r"(SDC)\s*[\=\:]\s*([\d.]+)",
		"not_together":r"(cannot_be_together)\s*:\s*([{\w\-,\s}]*})",
		"must_have":r"(must-have)\s*:\s*([\w\s(or)]+)",
		"not_together_elements":r"\{*'*([\w-]+),*\s*([\w-]+)'*\}*",
		"not_together_split":r"\}\s*,\s*\{",
		"transaction":r"([\w-]+)"
	}

	def __new__(cls, *args, **kwargs):  
		if not cls.__instance:  
			cls.__instance = object.__new__(Preprocess)
		return cls.__instance 

	def preprocessConstraints(self, constraints):
		if constraints == []:
			return constraints
		processedConstraints = {}
		for line in constraints:
			MIS = re.match(self._patterns['MIS'], line)
			if(MIS):
				processedConstraints[MIS.group(1).lower()] = float(MIS.group(2))
			SDC = re.match(self._patterns['SDC'], line)
			if(SDC):
				processedConstraints[SDC.group(1).upper()] = float(SDC.group(2))
			not_together = re.match(self._patterns['not_together'],line)
			if(not_together):
				not_together_split = re.split(self._patterns['not_together_split'],not_together.group(2))
				not_together_elements = []
				for i in not_together_split:
					match = re.match(self._patterns['not_together_elements'],i)
					not_together_elements.append((match.group(1).strip().lower(), match.group(2).strip().lower()))
				processedConstraints['not_together'] = not_together_elements
			must_have = re.match(self._patterns['must_have'],line)
			if(must_have):
				processedConstraints['must_have'] = [i.strip().lower() for i in must_have.group(2).split("or")]
			others = re.match(self._patterns['others'],line)
			if(others):
				processedConstraints[others.group(1)] = float(others.group(2))
		if not 'not_together' in processedConstraints:
			processedConstraints['not_together'] = ""
		if not 'must_have' in processedConstraints:
			processedConstraints['must_have'] = ""	
		return processedConstraints

	def preprocessTransaction(self, transaction):
		if transaction == "":
			return transaction
		processedTransaction = [i.strip().lower() for i in re.findall(self._patterns["transaction"], transaction)]
		return processedTransaction
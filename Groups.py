
# Groups module for PythoBB
# 1 must be Administrator, and 2 must be Default user.
# Do NOT edit group 1, if you do it may reassign the two
# values, and users who are in the second user group
# (default) will have administrator permissions.

Groups = {
		1: {
			"Name":        "Administrator",
			"Description": "Site administrator.",
			"Style":       "color:#F00;text-shadow:0 0 5px #EE3535;"
		},
		2: {
			"Name":        "Default user",
			"Description": "Forum member",
			"Style":       ""
		}
	}

#
# stdlib
#
import unittest
#
# jsonstat
#
import jsonstat


class TestDimension(unittest.TestCase):

    def setUp(self):
        self.json_string_index='''
		{
			"label" : "2003-2014",
			"category" : {
				"index" : {
					"2003" : 0,
					"2004" : 1,
					"2005" : 2,
					"2006" : 3,
					"2007" : 4,
					"2008" : 5,
					"2009" : 6,
					"2010" : 7,
					"2011" : 8,
					"2012" : 9,
					"2013" : 10,
					"2014" : 11
				}
			}
		}
		'''

        self.json_string_hole_in_index='''
		{
			"label" : "2003-2014",
			"category" : {
				"index" : {
					"2003" : 0,
					"2004" : 1,
					"2005" : 2,
					"2006" : 3,
					"2011" : 8,
					"2012" : 9,
					"2013" : 10,
					"2014" : 11
				}
			}
		}
		'''

        self.json_string_size_one='''
            {
			    "label" : "country",
			    "category" : {"label" : { "CA" : "Canada" }}
			}
		'''


        self.json_string_label_and_indes='''
        	{
		        "label" : "OECD countries, EU15 and total",
		        "category" : {
		            "index" : { "AU" : 0, "AT" : 1, "BE" : 2, "IT": 3 },
                    "label" : { "AU" : "Australia", "AT" : "Austria", "BE" : "Belgium", "CA" : "Canada", "IT":"Italy" }
                }
            }
        '''


    def test_getters(self):
        dim = jsonstat.JsonStatDimension("test_dim", 10, 0, 'role')
        self.assertEquals(dim.name(), "test_dim")
        self.assertEquals(dim.size(), 10)
        self.assertEquals(dim.pos(), 0)
        self.assertEquals(dim.role(), "role")

    def test_exception_not_valid(self):
        dim = jsonstat.JsonStatDimension("year", 10, 0, None)
        with self.assertRaises(jsonstat.JsonStatException):
            r = dim.idx2pos('2013')

    def test_exception_size(self):
        dim = jsonstat.JsonStatDimension("year", 10, 0, None)

        with self.assertRaises(jsonstat.JsonStatException):
            dim.from_string(self.json_string_index)

    def test_exception_hole_in_category_index(self):
        dim = jsonstat.JsonStatDimension("year", 8, 0, None)
        with self.assertRaises(jsonstat.JsonStatException) as cm:
            dim.from_string(self.json_string_hole_in_index)

        e = cm.exception
        self.assertEquals(e.value, "index 11 for dimension 'year' is greater than size 8")

    def test_size_one(self):
        dim = jsonstat.JsonStatDimension("country", 1, 0, None)
        dim.from_string(self.json_string_size_one)
        self.assertEqual(u'country', dim.label())
        self.assertEqual(1, len(dim))

    def test_idx2pos(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_string_index)
        self.assertEquals(dim.idx2pos("2003"), 0)
        self.assertEquals(dim.idx2pos("2014"), 11)

    def test_pos2idx(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_string_index)
        self.assertEquals(dim.pos2idx(0), "2003")
        self.assertEquals(dim.pos2idx(11), "2014")

    def test_get_index(self):
        dim = jsonstat.JsonStatDimension("year", 12, 0, None)
        dim.from_string(self.json_string_index)
        expected = ['2003', '2006', '2007', '2004', '2005', '2014', '2008', '2009', '2011', '2010', '2013', '2012']
        result = dim.get_index()
        self.assertEquals(expected, result)

    def test_exception_mismatch_index_and_label(self):
        dim = jsonstat.JsonStatDimension("year", 4, 0, None)
        with self.assertRaises(jsonstat.JsonStatMalformedJson) as cm:
            dim.from_string(self.json_string_label_and_indes)

        e = cm.exception
        expected = "dimension 'year': mismatch between indexes 4 and labels 5"
        self.assertEquals(e.value, expected)

if __name__ == '__main__':
    unittest.main()

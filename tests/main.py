"""
 EEWMap - Tests - Main
 Used to check the status of:
    - Utilities, including:
        - response_verify
        - generate_list
        - relpath
    - Modules, including:
        - area
        - centroid
        - intensity
        - pswave
    Note: The station to English module isn't currently being used, so it won't be tested.
"""
# noinspection PyUnresolvedReferences
from app import app  # In order to pre-initialize the application
from classes import DemoNormIntensityJson, \
    DemoIntAbnIntensityJson, DemoAreaAbnIntensityJson, DemoNormTsunamiJson, DemoGradeAbnTsunamiJson, \
    DemoAreaAbnTsunamiJson
from config import VERSION

import sys
import unittest

import HTMLReport

sys.path.append('../')


class TestUtilities(unittest.TestCase):
    """The tests for utilities."""

    def test_generate_list(self):
        """
        Tests generate_list with four samples.
            - Just a string "123" -> ["123"]
            - A list ["123", "456"] -> ["123", "456"]
            - An empty string "" -> []
            - A False -> []
        """
        from modules.sdk import generate_list
        self.assertEqual(generate_list("123"), ["123"])
        self.assertEqual(generate_list(["123", "456"]), ["123", "456"])
        self.assertEqual(generate_list(""), [])
        self.assertEqual(generate_list(False), [])

    def test_relpath(self):
        """
        Tests relpath by reading test_file.txt.
        If the content isn't "TEST", then the function is broken.
        """
        from modules.sdk import relpath
        path_to_test_file = relpath("./test_file.txt")
        self.assertNotEqual(path_to_test_file, "")
        fp = open(path_to_test_file, "r+")
        content = fp.read()
        self.assertEqual(content, "TEST")
        fp.close()


class TestModules(unittest.TestCase):
    def setUp(self) -> None:
        """
        Sets up GeoJson instance and checks GeoJson's initialization.
        """
        from modules.area import geojson_instance
        self.geojson_instance = geojson_instance
        self.assertNotEqual(self.geojson_instance.japan_areas, {})
        self.assertNotEqual(self.geojson_instance.tsunami_areas, {})

    def test_area_coloring(self):
        """
        Tests get_intensity_json function.
        """
        normal_geojson = self.geojson_instance.get_intensity_json(DemoNormIntensityJson.area_names,
                                                                  DemoNormIntensityJson.area_intensities)
        intensity_abnormal_geojson = self.geojson_instance.get_intensity_json(DemoIntAbnIntensityJson.area_names,
                                                                              DemoIntAbnIntensityJson.area_intensities)
        area_abnormal_geojson = self.geojson_instance.get_intensity_json(DemoAreaAbnIntensityJson.area_names,
                                                                         DemoAreaAbnIntensityJson.area_intensities)
        self.assertEqual(normal_geojson["features"][0]["properties"]["intensity"], "5+")
        self.assertEqual(intensity_abnormal_geojson["features"][0]["properties"]["intensity"], "0")
        self.assertEqual(area_abnormal_geojson["features"], [])
        self.assertEqual(normal_geojson["features"][0]["properties"]["intensity_color"],
                         DemoNormIntensityJson.intensity_color)
        self.assertEqual(intensity_abnormal_geojson["features"][0]["properties"]["intensity_color"],
                         DemoIntAbnIntensityJson.intensity_color)

    def test_tsunami_coloring(self):
        """
        Tests get_tsunami_json function.
        """
        normal_tsunami_geojson = self.geojson_instance.get_tsunami_json(DemoNormTsunamiJson.area_names,
                                                                        DemoNormTsunamiJson.area_grades)
        grade_abnormal_geojson = self.geojson_instance.get_tsunami_json(DemoGradeAbnTsunamiJson.area_names,
                                                                        DemoGradeAbnTsunamiJson.area_grades)
        area_abnormal_geojson = self.geojson_instance.get_tsunami_json(DemoAreaAbnTsunamiJson.area_names,
                                                                       DemoAreaAbnTsunamiJson.area_grades)
        self.assertEqual(normal_tsunami_geojson["features"][0]["properties"]["grade"], "MajorWarning")
        self.assertEqual(area_abnormal_geojson["features"], [])
        self.assertFalse("intensity_color" in grade_abnormal_geojson["features"][0]["properties"])

    def test_centroids(self):
        """
        Checks whether the centroids are empty or not.
        """
        from modules.centroid import centroid_instance
        self.assertNotEqual(centroid_instance.station_centroid, {})
        self.assertNotEqual(centroid_instance.area_centroid, {})
        self.assertNotEqual(centroid_instance.earthquake_station_centroid, {})

    def test_intensity_to_color(self):
        """
        Tests intensity_to_color function by reading 'test_intensity_to_color.gif' file.
        This file is all red, representing intensity 7.0.
        So, all the intensity stations' detailed_intensity should be 7.0, intensity should be "7".
        """
        from modules.intensity import intensity2color
        with open("./test_intensity_to_color.gif", "rb") as f:
            resp_raw = f.read()
            f.close()
        int2color_response = intensity2color(resp_raw)
        self.assertNotEqual(int2color_response, {})
        self.assertTrue("ABSH01" in int2color_response)
        self.assertEqual(int2color_response["ABSH01"]["detail_intensity"], 7.0)
        self.assertEqual(int2color_response["ABSH01"]["intensity"], "7")

    def test_pswave(self):
        """
        Tests parse_swave function with five examples.
            - Normal (depth: 30, time_passed: 225) -> 969.---
            - Depth abnormal (depth: 1000, time_passed: 0) -> None
            - Time abnormal (depth: 0, time_passed: 200000) -> None
            - No depth corresponding (depth: 162.25, time_passed: 0) -> None
            - No s1, s2 (intermediate value) corresponding (depth: 170, time_passed: 0) -> None
        """
        from modules.pswave import parse_pswave
        normal_time = parse_pswave(30, 225)[0]
        depth_abnormal_time = parse_pswave(1000, 0)[0]
        time_abnormal_time = parse_pswave(0, 200000)[0]
        no_depth_corresponding_time = parse_pswave(162.25, 0)[0]
        no_s1_s2_time = parse_pswave(170, 0)[0]
        self.assertEqual(normal_time, 969.3970522554712)
        self.assertEqual(depth_abnormal_time, None)
        self.assertEqual(time_abnormal_time, None)
        self.assertEqual(no_depth_corresponding_time, None)
        self.assertEqual(no_s1_s2_time, None)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUtilities))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestModules))
    runner = HTMLReport.TestRunner(title='EEWMap (v{}) Test Report'.format(VERSION),
                                   sequential_execution=True
                                   )
    runner.run(suite)

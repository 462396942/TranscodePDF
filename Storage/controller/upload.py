# -*- coding: utf-8 -*-
import requests, os


def upload(url=None, target_file_path=None, path=None):

	fileName = os.path.basename(target_file_path)
	files = {"file1": (fileName, open(target_file_path, 'rb'), "multipart/form-data")}

	data = {"custom_path": path}
	session = requests.post(url, data=data, files=files)
	return session.text
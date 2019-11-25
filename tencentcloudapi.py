from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.nlp.v20190408 import nlp_client, models 

with open("./credential.txt", 'r') as f:
	cre1 = f.readline().strip()
	cre2 = f.readline().strip()

def word_similarity(src_wrd, tar_wrd):
	try: 
		cred = credential.Credential(cre1, cre2) 
		httpProfile = HttpProfile()
		httpProfile.endpoint = "nlp.tencentcloudapi.com"

		clientProfile = ClientProfile()
		clientProfile.httpProfile = httpProfile
		client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

		req = models.WordSimilarityRequest()
		params = '{}'
		req.from_json_string(params)
		req.SrcWord = src_wrd
		req.TargetWord = tar_wrd

		resp = client.WordSimilarity(req) 
		print(resp.to_json_string()) 

	except TencentCloudSDKException as err: 
		print(err) 

def text_similarity(src_txt, tar_txt):
	try: 
		cred = credential.Credential(cre1, cre2) 
		httpProfile = HttpProfile()
		httpProfile.endpoint = "nlp.tencentcloudapi.com"

		clientProfile = ClientProfile()
		clientProfile.httpProfile = httpProfile
		client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

		req = models.SentenceSimilarityRequest()
		params = '{}'
		req.from_json_string(params)
		req.SrcText = src_txt
		req.TargetText = tar_txt

		resp = client.SentenceSimilarity(req) 
		print(resp.to_json_string()) 

	except TencentCloudSDKException as err: 
		print(err) 

def split_sentence(sen):
	try: 
		cred = credential.Credential(cre1, cre2) 
		httpProfile = HttpProfile()
		httpProfile.endpoint = "nlp.tencentcloudapi.com"

		clientProfile = ClientProfile()
		clientProfile.httpProfile = httpProfile
		client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

		req = models.LexicalAnalysisRequest()
		params = '{}'
		req.from_json_string(params)
		req.Text = sen

		resp = client.LexicalAnalysis(req) 
		print(resp.to_json_string()) 

	except TencentCloudSDKException as err: 
		print(err) 


if __name__=='__main__':
	word_similarity("广发银行", "银行业")
	word_similarity("CFA", "财务会计")
	text_similarity("CFA", "注册会计分析师")
	text_similarity("广发银行---业务专员", "银行业")
	split_sentence("广发银行---业务专员")
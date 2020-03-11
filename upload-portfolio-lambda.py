import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns=boto3.resource('sns')
    topic=sns.Topic('arn:aws:sns:us-east-1:524339592450:deployPorfolioTopic')
    try:
        #session = boto3.Session(profile_name='eiskraxlerportfolio')
        s3bucket = boto3.resource('s3')
        
        portfolio_bucket=s3bucket.Bucket('portfolio.stefanbauer.solutions')
        build_bucket=s3bucket.Bucket('portfoliobuild.stefanbauer.solutions')
        
        
        portfolio_zip=io.BytesIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
        
        
        
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj=myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
                
        topic.publish(Subject="Porfolio Deployment",Message="Portfolio deployed successfully")
    except:
        topic.publish(Subject="Porfolio Deployment Faild",Message="Portfolio was NOT deployed successfully!!")
        raise
    return 'Hello from Lambda'
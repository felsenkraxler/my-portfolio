import boto3
import io
import zipfile
import mimetypes

session = boto3.Session(profile_name='eiskraxlerportfolio')
s3bucket = session.resource('s3')

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
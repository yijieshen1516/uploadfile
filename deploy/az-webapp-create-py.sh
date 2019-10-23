
az webapp config appsettings set -g "$pe-peproto-south_central_us" -n "$peuploadpressure" --settings "SCM_DO_BUILD_DURING_DEPLOYMENT=true"
az webapp deployment source config-zip -g "$pe-peproto-south_central_us" -n "$peuploadpressure" --src ./deploy.zip
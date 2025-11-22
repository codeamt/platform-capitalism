**README summary for deployment**

 **1. Build & push the image:**

```
bash lightsail_build.sh
```

**2. Deploy container to Lightsail:**


```
bash deploy_lightsail.sh
```

**3. Monitor logs**

` aws lightsail get-container-log --service-name platform-simulation --region us-east-1`


**4. Access your app via the Lightsail public endpoint printed after deployment.**

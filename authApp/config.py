#!/usr/bin/python
# -*- coding:utf-8 -*-


# 支付宝登录配置
class Alipay:

    def __init__(self, is_sandbox=False):
        self.is_sandbox = is_sandbox
        self._sandbox = {
            "APP_ID": "2016102600765170",
            "REDIRECT_URI": "http://www.gf-app.cn:8000/auth/signin/alipay/token",
            "GATEWAY": "https://openauth.alipaydev.com/oauth2/publicAppAuthorize.htm?app_id=%s&scope=auth_user&redirect_uri=%s&state=init",
            "PRIVATE_KEY": "MIIEowIBAAKCAQEAhyE6eSUxtCsYmAka1DGasl7DjiLo0tbbjbAXsILnvCs0XNNi153eGUZCqM+qlWAnwa6+GlOVIBi7HiymkkJrsbPNwJQ5pZBoEaU2maHEEh6pHi40z7us+d6kwpoxZO4tO18FX2RDQkU8xrk1nq6C0pl5VdHl5gkcucwGt5oHDgGYpopSVeOy1BxvO9aXXPrvZ/gil6EO5DWATP5dH1gsI0dnbigz1Zu8u/yIh8A15S4YqOFzfhV43Gk3wFXRXBGv2bYNmFylfU/9820NfALMcMNlU0ZUs5F+QwNiTywbF4d6SdCZPQ3CMohTpA/SCwwo/EVMEq9yBA4iBZfUg4aNTQIDAQABAoIBAFIuOjKNFUJeZ1GnT+K23D8YdNPPlUsMknAEJRQbOLXujKTbhiRdhUJXwZiK21KHLQaUsFaweGQRxlLektsme/qRwFMbkkeHoFMC6Ebc47KlZPLO5R1lJRi9d/RF9D5Ov8F403qlLmZyVzkAUITV2wgbgHhZ8/hHmGnClF861ImGOJttcbIPM2kAr1BtUfL2oIlfsmZdduePlIlMJLyI0a1nYAeqHXEDqDEBK7DfqxVxwAqN0BG0C2Icu2MQ6s8OCL4gAbDet2+w9FueIIx6x+xvdzsdQ9LEBdARrpcYyCZTVLVU8+VQFnANwW3KBOco9IpdWNJnBjb/I+Me4buW5p0CgYEA1ZTg5fVXTWrleCp8suoIJXLZAKJetn/jHeT3ua7QaDCTSmz7LCcP4z8I06hvHuYWMDVoJmYhDzXQQhuFXIyVX41kmc3/Qz8sg0S0iTIJjjv5fVa4w6GpJeEp5Na9cGcnK89Vipv+EEjnzH47WMjjkPQWhfYgxHqcWJMvKrSvWU8CgYEAofehFEHd2WBTILUF/kR7IeAAXJfGGQd5i2lMu2SS2Z/Gv/ysJxBHBrU6Rw8EjdiiPh5bkLRsfUqK+TqnUw7ZYJRNSpnPnTqFG6G/695AgnSIumYn+Z9rVnyi9huhha3eP259vzUfoCIIQxfORwlAhXYMVtQ0IsZr+zXZJKaIUKMCgYAmsYchAhaj5ubVo1TeEPoS1sCrlb707yxVQSMEF8CX75zvkdjbQeRl9giCV/Rxs5t3dmV892mr2ML3BwddIfb5zaLZHnHNXAeTbIIMjO0gQItNgsWMY6BCRY2ScLj3QSjejfxgVSxtBNhBuujDh/l6TE48TL/Y+KGUhm24He3ajwKBgGa2nE81ahRFctImGpPiJ9gWrwQJOBZ9WAYiFAguwrYCDk+IVEA9oV1OppOToYa24ETWiajd0oMuN63QFXalzxLhWZa6rh/+kZUxYX2aJ3zTnDXhPO6fu7lQNyQt56PX3D6LunD8pn6ttmGeAjGoW2OHtlGGJz36aVYZEwicF4xTAoGBAKaF5ehB/pw2DGQAQ5svJnlDk/ClTOf2DQXo4QDBoq1yrEflyZqpmAInmAq1vFhPs/qC78rFRKE5tsT0mP62AAuaV51/xcR+LSlnGkwbXTvQqtasHjOEpHvHmxKauTd8MHPxUELY7vxlqtg81rDjOPrunWaJrEYTDbrTtzAfqEZ2",
            "PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhyE6eSUxtCsYmAka1DGasl7DjiLo0tbbjbAXsILnvCs0XNNi153eGUZCqM+qlWAnwa6+GlOVIBi7HiymkkJrsbPNwJQ5pZBoEaU2maHEEh6pHi40z7us+d6kwpoxZO4tO18FX2RDQkU8xrk1nq6C0pl5VdHl5gkcucwGt5oHDgGYpopSVeOy1BxvO9aXXPrvZ/gil6EO5DWATP5dH1gsI0dnbigz1Zu8u/yIh8A15S4YqOFzfhV43Gk3wFXRXBGv2bYNmFylfU/9820NfALMcMNlU0ZUs5F+QwNiTywbF4d6SdCZPQ3CMohTpA/SCwwo/EVMEq9yBA4iBZfUg4aNTQIDAQAB",
            "ALIPAY_PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwMOreBfo7EBHtX9OSHdb4Bfp07UGUeKKamhRV9+MIOjhEExJYZgdTb0pirYVbf5vgTiXOwhOGotSnkTANHuDe9Ys8zKriYEEZt91u0x66EZD8dRIUXVtwCvU3qPPXZycLVAs255uw9QtwpvQ/Q4i4OTkvapFLps4NknZi9VoSEsTtXny4CwXPgDmo9Sn2KWGoD/S3pXlxhHk1qhRYFpVFxQXH2CimJUJwMfVw7YxuAWEidSVN4Cle1DRPSp6IasHi+B0bJ55njPgIoCEzsq7E9J3gnRKnY4s7TNytINZiUNOiS5NkN9KsZQlZ0C46EFiF1YDUTvVAQP+7XD9r7sT3wIDAQAB",
        }
        self._production = {
            "APP_ID": "2021001171660880",
            "REDIRECT_URI": "http://www.gf-app.cn:8000/auth/signin/alipay/token",
            "GATEWAY": "https://openauth.alipay.com/oauth2/publicAppAuthorize.htm?app_id=%s&scope=auth_user&redirect_uri=%s&state=init",
            "PRIVATE_KEY": "MIIEowIBAAKCAQEAnCTthUKqPa2LgO8PVI4cVsFEJBJQUCbSKU43W2Vpyk7ktTSXDz2wx4jXwCbWUd4rNnyhBJzAZxSEtQpWXHORmX/5sorBB/L0rYejtWLPrA7pdDtujDyXMBd4T7kTocvXroegsb43POxo3puYVFWoPcQM+uTmluQlz/LLslFDUqV6rMGt21AdDf35ukoq8Eomg5RtIEojS7DgI2y7muPgxg5EA7Rge1ASXNXEH7Jueq49HkpGaiC6Rhs+NTxQf5gUTVzKhzC1s1AOu2DE30RwVUhJ047/uKtG6wIZiHUQIqOGSrV9ynpkWbLpUNEHshVYo1damnJfu5I+EgXRt9eeZQIDAQABAoIBABoTEJbwSv2BvYoKYcT89j6Gh5p+dGruEKpVJWldxgzCn+6imZcx9hNcBqtP0Ppa31x582mRw49zHbYdw84sfmPjuw7VnOZ26+UOgYgIuCVDWDjQs+U3OQgO40hs35plL981RuBno1HJKLoDwaxToYSu+HvtPZR1BNt08A8XAucJ96nmyu/IE1bP10afT8+SDoB6JfuJJiYImXX+qI7zvg5XRaa0rrUyTI0rQhSI+mR0BesV/h1064ZC2wEi+4+n9T3q8mgw9DHV/okR41KKAQB6M7clUD36v8MOCBrxF90Tua9ag5Da+5RIHC/q7+CfqU8IW8SWyImBmMmC5TB6oAECgYEA6G6cfz6C8IU/ZtiSeLXMLBUtcwUuCXFiNu33lBpHMM3onijJSqNfWizqHPlKm7b2dIQvd7x3O88E+GtF86ZrVC7QkPb4xvX3UakzM7JgHoQIgd5n7FFV0moaleIkS5G0DUFN/xvA3Ic9FJvFFoBQsZTxFoT+OMVJuOZIDpeUIAUCgYEAq/oQe+6yJ1IG2jdFZMfsDvTvzu6XkgMhwrEml3b3tGltCjTgGtopkUaReL7ZQHxFA8HfdSW7P7Nh2GizEk6c6qYHWg0lTb0buVmnSfXv1s/dQBEC+SC20V+lYcFsBhsk1ciOuY0TEHKPpPy9WbgkO6vtf6n6lP2IF5/dmwAUsuECgYEAtvtthNcnqkacVVEmbpVguUuqziRDy/dRRMEu6Y+OgCN6gBjH71SSmqFFZa30SIZPnAb8f50FmTYvSYraNSjM0idQ1u83hxrYq5cy0f4Zoax8LhFzax3VHKOfbmPsAvof71d8Gdw1hueI9JJ1JHO8EzGYYwwsP3FByqiwDZzTZikCgYAnI4MK4Xj0D+v1T6zgUct8X+wPuScPmNzfFTgGMpIPIgspznzOP6ZEJL5Ir4576Yw/XakAXTTvO2DiQnm2ieOWV3DG4sUBmy8rEKdM4sbRqX7d7MEzd2mD3vOhesad4SGR8dHhkqSrEpd0Yfyp5YmBdxBXBJU9wTFuxvhFJVCQoQKBgAsqrH4rDJFPrUS+BEInzAEnADLI/pm1teKfXCd5vid+nHyUD4b+c6zGITOFsLKYT6WqTdQYYfqA3bCw5IVgS0L9uAA5scqIw3XBBawae05P8iv3OMQpM/wRxHwHybbpTGa9uZmc77RyAd96+HyFwCiyCcmD2J7/OQQoaYWqk9EJ",
            "PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnCTthUKqPa2LgO8PVI4cVsFEJBJQUCbSKU43W2Vpyk7ktTSXDz2wx4jXwCbWUd4rNnyhBJzAZxSEtQpWXHORmX/5sorBB/L0rYejtWLPrA7pdDtujDyXMBd4T7kTocvXroegsb43POxo3puYVFWoPcQM+uTmluQlz/LLslFDUqV6rMGt21AdDf35ukoq8Eomg5RtIEojS7DgI2y7muPgxg5EA7Rge1ASXNXEH7Jueq49HkpGaiC6Rhs+NTxQf5gUTVzKhzC1s1AOu2DE30RwVUhJ047/uKtG6wIZiHUQIqOGSrV9ynpkWbLpUNEHshVYo1damnJfu5I+EgXRt9eeZQIDAQAB",
            "ALIPAY_PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkGK7XxTWnPbNP+m+PD9+coOCvU5mJOXsHy0Kv+wjI4qzFHB8EvmFgOtkG58b8+lu0YzV/seidDw3Ny7MXYSfs9rmcUWQC4Xp3quj/W2oWael263KgMChdLYCT21ATl2EpJI9uMqp0uiI/r2o/vEg4Kj3p4TnGmF34O5g2smuYw3WU2w8InxjNrvnUBbds0SLU1Bn/8pj41NfUyd4lqQmo2iSrHErsHEpl856qTZFuYSZaN+Y66I/TfeyDCQ6gBVs3kkcVNiIVo0A5LW2jnD5xcSJB8zfwq0VlEdCSx+V81cMe/o1rgZpO4YlJNLIRLUrUzI+Pnf6+l5gQY3QiPcaOwIDAQAB",
        }

    @property
    def APP_ID(self):
        return self._sandbox["APP_ID"] if self.is_sandbox else self._production["APP_ID"]

    @property
    def REDIRECT_URI(self):
        return self._sandbox["REDIRECT_URI"] if self.is_sandbox else self._production["REDIRECT_URI"]

    @property
    def GATEWAY(self):
        return self._sandbox["GATEWAY"] if self.is_sandbox else self._production["GATEWAY"]

    @property
    def PRIVATE_KEY(self):
        return self._sandbox["PRIVATE_KEY"] if self.is_sandbox else self._production["PRIVATE_KEY"]

    @property
    def PUBLIC_KEY(self):
        return self._sandbox["PUBLIC_KEY"] if self.is_sandbox else self._production["PUBLIC_KEY"]

    @property
    def ALIPAY_PUBLIC_KEY(self):
        return self._sandbox["ALIPAY_PUBLIC_KEY"] if self.is_sandbox else self._production["ALIPAY_PUBLIC_KEY"]
# 微信登录配置
class Wx:
    pass
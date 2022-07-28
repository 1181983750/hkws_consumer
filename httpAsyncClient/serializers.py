from typing import Type

from rest_framework import serializers

from httpAsyncClient.models import hkws_xf_xfmx, hkws_xf_ygye, rs_ygxx, hkws_xf_btmd


class hkws_xf_xfmxModelSerializer(serializers.ModelSerializer):
    ygdm = serializers.SerializerMethodField()
    ygmc = serializers.SerializerMethodField()
    pym = serializers.SerializerMethodField()
    class Meta:
        model = hkws_xf_xfmx  # 使用的数据表模型
        fields = '__all__'

    def selcet_info(self, ygid: int):
        return rs_ygxx.objects.get(ygid=ygid)

    def get_ygdm(self, obj: Type[hkws_xf_xfmx]):
        return self.selcet_info(obj.ygid).ygdm

    def get_ygmc(self, obj: Type[hkws_xf_xfmx]):
        return self.selcet_info(obj.ygid).ygmc

    def get_pym(self, obj: Type[hkws_xf_xfmx]):
        return self.selcet_info(obj.ygid).pym


class hkws_xf_ygyeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = hkws_xf_ygye
        fields = '__all__'


class rs_ygxxModelSerializer(serializers.ModelSerializer):
    # ye = serializers.SerializerMethodField()
    class Meta:
        model = rs_ygxx
        fields = ['ygid','ygdm','ygmc','pym','xb','bmmc','bmmc1','bmmc2','bmmc3','hkws_rlbs']

    def get_ye(self, obj):
        try:
            ye = hkws_xf_xfmx.objects.get(ygid=obj.id).ye
        except:
            ye = 0.00
        return ye


class hkws_xf_btmdModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = hkws_xf_btmd
        fields = '__all__'




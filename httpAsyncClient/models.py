from django.db import models

from public.utils.BaseOrm import BaseModel


class hkws_xf_sbmx(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    sbmc = models.CharField(db_column='sbmc', max_length=50, blank=True, null=True, verbose_name='设备名称', )
    sbip = models.CharField(db_column='sbip', max_length=50, blank=True, null=True, verbose_name='设备ip', )
    sblxid = models.IntegerField(db_column='sblxid', blank=True, null=True, verbose_name='设备类型id', )
    sblxmc = models.CharField(db_column='sblxmc', max_length=50, blank=True, null=True, verbose_name='设备类型名称', )
    sbickqyid = models.IntegerField(db_column='sbickqyid', blank=True, null=True, verbose_name='设备ic卡区域id', )
    sbqymc = models.CharField(db_column='sbqymc', max_length=50, blank=True, null=True, verbose_name='设备区域名称', )
    userid = models.CharField(db_column='userid', max_length=50, blank=True, null=True, verbose_name='登录名', )
    password = models.CharField(db_column='pass', max_length=50, blank=True, null=True, verbose_name='密码', )
    ty = models.BooleanField(db_column='ty', blank=True, null=True, default=False,verbose_name='是否停用',)
    bz = models.CharField(db_column='bz', max_length=255, blank=True, null=True, verbose_name='备注', )
    xlh = models.CharField(db_column='xlh', max_length=100, blank=True, null=True, verbose_name='序列号', )

    class Meta:
        db_table = 'hkws_xf_sbmx'
        verbose_name = '海康威视消费机明细'
        managed = False


class hkws_xf_sbygxx(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    ygid = models.IntegerField(db_column='ygid', blank=True, null=True, verbose_name='员工id', )
    sbid = models.IntegerField(db_column='sbid', blank=True, null=True, verbose_name='设备id', )
    issuccess = models.BooleanField(db_column='issuccess', blank=True, null=True, verbose_name='是否下发成功 1生效、0失效', )

    class Meta:
        db_table = 'hkws_xf_sbygxx'
        verbose_name = '员工对应消费机设备'
        managed = False

class hkws_xf_ygye(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    ygid = models.IntegerField(db_column='ygid', blank=True, null=True, verbose_name='员工id', unique=True)
    ye = models.DecimalField(db_column='ye',max_digits=19,decimal_places=4, blank=True, null=True, verbose_name='余额', )

    class Meta:
        db_table = 'hkws_xf_ygye'
        verbose_name = '员工余额'
        managed = False
        # unique_together = ['ygid']  #联合唯一

class hkws_xf_xfmx(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    sbxh = models.IntegerField(db_column='sbxh', blank=True, null=True, verbose_name='设备型号', )
    sbip = models.CharField(db_column='sbip',max_length=64,blank=True,null=True,verbose_name='设备ip')
    ygid = models.IntegerField(db_column='ygid',blank=True,null=True,verbose_name='员工id')
    ygdm = models.CharField(db_column='ygdm',max_length=64,blank=True,null=True,verbose_name='员工代码')
    ygmc = models.CharField(db_column='ygmc',max_length=64,blank=True,null=True,verbose_name='员工名称')
    xfje = models.DecimalField(db_column='xfje',max_digits=12,decimal_places=4, blank=True, null=True, verbose_name='消费或充值金额', )
    ye = models.DecimalField(db_column='ye',max_digits=19,decimal_places=4, blank=True, null=True, verbose_name='消费或充值后 余额', )
    xfrq = models.DateTimeField(db_column='xfrq', blank=True, null=True, verbose_name='消费日期', )
    sjrq = models.DateTimeField(db_column='sjrq', blank=True, null=True, verbose_name='事件日期', )
    xflx = models.IntegerField(db_column='xflx', blank=True, null=True, verbose_name='消费类型 1充值、2消费', )
    xflxmc = models.CharField(db_column='xflxmc', max_length=10, blank=True, null=True, verbose_name='消费类型名称 充值or消费', )
    sfbt = models.BooleanField(db_column='sfbt', blank=True, null=True, default=False ,verbose_name='是否报停',)
    serialNo = models.IntegerField(db_column='serialNo', blank=True, null=True, verbose_name='序列号', )
    verifyMode = models.CharField(db_column='verifyMode', max_length=10, blank=True, null=True, verbose_name='校验模式 默认存face', )
    nonce = models.CharField(db_column='nonce', max_length=50, blank=True, null=True, verbose_name='验证码', )
    czy = models.CharField(db_column='czy', max_length=50, blank=True, null=True, verbose_name='充值员', )
    bz = models.CharField(db_column='bz', max_length=80, blank=True, null=True, verbose_name='备注', )
    xlh = models.CharField(db_column='xlh', max_length=100, blank=True, null=True, verbose_name='序列号', )

    class Meta:
        db_table = 'hkws_xf_xfmx'
        verbose_name = '员工充值消费明细'
        managed = False


class hkws_yg_sbqy(BaseModel, models.Model):
    id = models.AutoField(primary_key=True)
    ygid = models.IntegerField(db_column='ygid', blank=True, null=True, verbose_name='员工id', )
    qyid = models.IntegerField(db_column='qyid', blank=True, null=True, verbose_name='海康威视区域id', )

    class Meta:
        db_table = 'hkws_yg_sbqy'
        verbose_name = '海康威视-->员工设备区域对应'
        managed = False


class rs_ygxx(models.Model):
    ygid = models.AutoField(db_column='id', primary_key=True)
    oldygid = models.IntegerField(db_column='oldygid', blank=True, null=True, verbose_name='erp员工id', )
    snowflake_id = models.BigIntegerField(db_column='snowflake_id', blank=True, null=True, verbose_name='Null', )
    ygdm = models.CharField(db_column='ygdm', max_length=10, blank=True, null=True, verbose_name='员工代码', )
    ygmc = models.CharField(db_column='ygmc', max_length=20, blank=True, null=True, verbose_name='员工名称', )
    pym = models.CharField(db_column='pym', max_length=10, blank=True, null=True, verbose_name='拼音码', )
    xb = models.CharField(db_column='xb', max_length=2, blank=True, null=True, verbose_name='性别', )
    mzdm = models.CharField(db_column='mzdm', max_length=10, blank=True, null=True, verbose_name='员工名族', )
    mzmc = models.CharField(db_column='mzmc', max_length=60, blank=True, null=True, verbose_name='名族名称', )
    ygjg = models.CharField(db_column='ygjg', max_length=30, blank=True, null=True, verbose_name='员工籍贯', )
    fjlx = models.CharField(db_column='fjlx', max_length=10, blank=True, null=True, verbose_name='户籍类型', )
    zzmm = models.CharField(db_column='zzmm', max_length=10, blank=True, null=True, verbose_name='群众面貌', )
    hyqk = models.CharField(db_column='hyqk', max_length=10, blank=True, null=True, verbose_name='婚姻情况', )
    jkz = models.BooleanField(db_column='jkz', blank=True, null=True, verbose_name='健康证', default=False)
    tj_rz = models.BooleanField(db_column='tj_rz', blank=True, null=True, verbose_name='入职体检', default=False)
    tj_lz = models.BooleanField(db_column='tj_lz', blank=True, null=True, verbose_name='离职体检', default=False)
    zglb = models.CharField(db_column='zglb', max_length=10, blank=True, null=True, verbose_name='职工类别', )
    jszcdm = models.CharField(db_column='jszcdm', max_length=10, blank=True, null=True, verbose_name='技术职称代码', )
    jszcmc = models.CharField(db_column='jszcmc', max_length=60, blank=True, null=True, verbose_name='技术职称名称', )
    zlfd = models.CharField(db_column='zlfd', max_length=10, blank=True, null=True, verbose_name='资料分档', )
    jrgsjsr = models.CharField(db_column='jrgsjsr', max_length=20, blank=True, null=True, verbose_name='进入公司介绍人', )
    tjsrgx = models.CharField(db_column='tjsrgx', max_length=20, blank=True, null=True, verbose_name='同介绍人关系', )
    ygscff = models.BooleanField(db_column='ygscff', blank=True, null=True, verbose_name='员工手册发放', default=False)
    lrsj = models.BooleanField(db_column='lrsj', blank=True, null=True, verbose_name='老人手机', default=False)
    htksrq = models.DateField(db_column='htksrq', blank=True, null=True, verbose_name='合同开始日期', )
    htjsrq = models.DateField(db_column='htjsrq', blank=True, null=True, verbose_name='合同终止日期', )
    bmid = models.IntegerField(db_column='bmid', blank=True, null=True, verbose_name='部门id', )
    bmdm = models.CharField(db_column='bmdm', max_length=10, blank=True, null=True, verbose_name='部门代码', )
    bmmc = models.CharField(db_column='bmmc', max_length=60, blank=True, null=True, verbose_name='部门名称', )
    bmid1 = models.IntegerField(db_column='bmid1', blank=True, null=True, verbose_name='部门id1', )
    bmdm1 = models.CharField(db_column='bmdm1', max_length=10, blank=True, null=True, verbose_name='部门代码1', )
    bmmc1 = models.CharField(db_column='bmmc1', max_length=60, blank=True, null=True, verbose_name='部门名称1', )
    bmid2 = models.IntegerField(db_column='bmid2', blank=True, null=True, verbose_name='部门id2', )
    bmdm2 = models.CharField(db_column='bmdm2', max_length=10, blank=True, null=True, verbose_name='部门代码2', )
    bmmc2 = models.CharField(db_column='bmmc2', max_length=60, blank=True, null=True, verbose_name='部门名称2', )
    bmid3 = models.IntegerField(db_column='bmid3', blank=True, null=True, verbose_name='部门id3', )
    bmdm3 = models.CharField(db_column='bmdm3', max_length=10, blank=True, null=True, verbose_name='部门代码3', )
    bmmc3 = models.CharField(db_column='bmmc3', max_length=60, blank=True, null=True, verbose_name='部门名称3', )
    gwid = models.IntegerField(db_column='gwid', blank=True, null=True, verbose_name='岗位id', )
    gwdm = models.CharField(db_column='gwdm', max_length=10, blank=True, null=True, verbose_name='岗位代码', )
    gwmc = models.CharField(db_column='gwmc', max_length=60, blank=True, null=True, verbose_name='岗位名称', )
    gwjbdm = models.CharField(db_column='gwjbdm', max_length=10, blank=True, null=True, verbose_name='岗位级别代码', )
    gwjbmc = models.CharField(db_column='gwjbmc', max_length=60, blank=True, null=True, verbose_name='岗位级别名称', )
    xldm = models.CharField(db_column='xldm', max_length=10, blank=True, null=True, verbose_name='学历代码', )
    xlmc = models.CharField(db_column='xlmc', max_length=60, blank=True, null=True, verbose_name='学历名称', )
    jbdm = models.CharField(db_column='jbdm', max_length=10, blank=True, null=True, verbose_name='级别代码', )
    jbmc = models.CharField(db_column='jbmc', max_length=60, blank=True, null=True, verbose_name='级别名称', )
    qymc = models.CharField(db_column='qymc', max_length=500, blank=True, null=True, verbose_name='考勤区域）弃用', )
    csny = models.DateField(db_column='csny', blank=True, null=True, verbose_name='出生日期', )
    jrgsrq = models.DateField(db_column='jrgsrq', blank=True, null=True, verbose_name='进入公司日期', )
    ygdgrq = models.DateField(db_column='ygdgrq', blank=True, null=True, verbose_name='员工调岗日期', )
    lxdz = models.CharField(db_column='lxdz', max_length=60, blank=True, null=True, verbose_name='联系地址', )
    lxdh = models.CharField(db_column='lxdh', max_length=20, blank=True, null=True, verbose_name='联系电话', )
    lxdh2 = models.CharField(db_column='lxdh2', max_length=20, blank=True, null=True, verbose_name='联系电话2', )
    lxdh_jtdh = models.CharField(db_column='lxdh_jtdh', max_length=20, blank=True, null=True, verbose_name='集团短号', )
    zjhm = models.CharField(db_column='zjhm', max_length=20, blank=True, null=True, verbose_name='证件号码（身份证', )
    syjyzbh = models.CharField(db_column='syjyzbh', max_length=30, blank=True, null=True, verbose_name='失业/就业证编号', )
    cjzbh = models.CharField(db_column='cjzbh', max_length=30, blank=True, null=True, verbose_name='残疾证编号', )
    sbkh = models.CharField(db_column='sbkh', max_length=30, blank=True, null=True, verbose_name='社保卡号', )
    ybkh = models.CharField(db_column='ybkh', max_length=30, blank=True, null=True, verbose_name='合作医疗证号', )
    zslx_mc = models.CharField(db_column='zslx_mc', max_length=200, blank=True, null=True, verbose_name='证书类型名称', )
    zslx_qt = models.CharField(db_column='zslx_qt', max_length=60, blank=True, null=True, verbose_name='证书类型其他', )
    upbj = models.CharField(db_column='upbj', max_length=10, blank=True, null=True, verbose_name='u盘标记', )
    bglry = models.BooleanField(db_column='bglry', blank=True, null=True, verbose_name='办公楼人员', default=False)
    sflz = models.BooleanField(db_column='sflz', blank=True, null=True, verbose_name='是否离职', default=False)
    lzrq = models.DateField(db_column='lzrq', blank=True, null=True, verbose_name='离职日期', )
    bz = models.CharField(db_column='bz', max_length=2147483647, blank=True, null=True, verbose_name='备注', )
    password = models.CharField(db_column='pass', max_length=255, blank=True, null=True, verbose_name='密码', )
    sx_czy = models.BooleanField(db_column='sx_czy', blank=True, null=True, verbose_name='是否操作员', default=False)
    sx_xsry = models.BooleanField(db_column='sx_xsry', blank=True, null=True, verbose_name='是否销售人员', default=False)
    wbdw = models.BooleanField(db_column='wbdw', blank=True, null=True, verbose_name='外包单位', default=False)
    qtwlry = models.BooleanField(db_column='qtwlry', blank=True, null=True, verbose_name='其他外来人员', default=False)
    gmbx = models.BooleanField(db_column='gmbx', blank=True, null=True, verbose_name='是否购买保险', default=False)
    cjrzrq = models.DateField(db_column='cjrzrq', blank=True, null=True, verbose_name='重计入职日期', )
    tyjr = models.BooleanField(db_column='tyjr', blank=True, null=True, verbose_name='退役军人', default=False)
    tyjr_cjrq = models.DateField(db_column='tyjr_cjrq', blank=True, null=True, verbose_name='参军日期', )
    tyjr_tyrq = models.DateField(db_column='tyjr_tyrq', blank=True, null=True, verbose_name='退役日期', )
    hkws_rlbs = models.BooleanField(db_column='hkws_rlbs', blank=True, null=True, verbose_name='是否采集人脸', default=False)
    zfsd = models.BooleanField(db_column='zfsd', blank=True, null=True, verbose_name='账户锁定', default=False)

    class Meta:
        db_table = 'rs_ygxx'
        verbose_name = '员工信息'
        managed = False


class hkws_xf_ip_whitelist(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(db_column='ip', max_length=50, blank=True, null=True, verbose_name='Null', )
    username = models.CharField(db_column='username', max_length=50, blank=True, null=True, verbose_name='Null', )

    class Meta:
        db_table = 'hkws_xf_ip_whitelist'
        verbose_name = '消费机ip白名单'
        managed = False


class hkws_xf_btmd(models.Model):
    id = models.AutoField(primary_key=True)
    ygid = models.IntegerField(db_column='ygid', blank=True, null=True, verbose_name='Null', )
    ygdm = models.IntegerField(db_column='ygdm', blank=True, null=True, verbose_name='Null', )
    ygmc = models.IntegerField(db_column='ygmc', blank=True, null=True, verbose_name='Null', )
    btje = models.DecimalField(db_column='btje', max_digits=19, decimal_places=4)
    bz = models.CharField(db_column='bz', max_length=50, blank=True, null=True, verbose_name='Null', )
    statusmsg = models.CharField(db_column='statusmsg', max_length=50, blank=True, null=True, verbose_name='Null', )

    class Meta:
        db_table = 'hkws_xf_btmd'
        verbose_name = '消费补贴名单'
        managed = False
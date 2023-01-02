# imports & globals
from config import config

from datetime import datetime, timezone
import time 

from tools.convert import utc2local

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model 
from passlib.hash import bcrypt, hex_md5



# Users
class User(Model):
    id = fields.IntField(pk=True)
    firstname = fields.CharField(80)
    email = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    admin_role = fields.BooleanField(Default=0)
    active = fields.BooleanField(Default=0)


    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def __str__(self):
        return f"id: {self.id}, firstname: {self.firstname}, email: {self.email}"

    def avatar(self, size=48) -> str:
        digest = hex_md5.hash(self.email.lower().encode('utf-8'))

        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def admin(self) -> int:
        if self.admin_role:
            return 1
        else:
            return 0       

    class Meta:
        table = "users"            

    class PydanticMeta:
        computed = ["admin", "avatar"]
              

User_Pydantic = pydantic_model_creator(User, name='User', exclude=("password_hash"))
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True, exclude=["admin_role", "active"])


# backends
class Backend(Model):

    id =  fields.IntField(pk=True)
    user_id = fields.IntField(null=False)
    backend = fields.CharField(10, null=False)
    backend_user = fields.CharField(80, null=False)
    backend_password =  fields.CharField(255, null=False)

    class Meta:
        table = "backend_credentials"
        unique_together=("user_id", "backend", "backend_user")


Backend_Pydantic = pydantic_model_creator(Backend, name='Backend')
BackendIn_Pydantic = pydantic_model_creator(Backend, name='BackendIn', exclude_readonly=True)


# Devices
# ----------------------------------------------------------------------------
class Device(Model):

    _ticks = 0

    device_id = fields.IntField(pk=True)
    backend_id = fields.IntField(null=False)
    device_extern_id =  fields.CharField(40, null=False)
    inserted_at = fields.DatetimeField  #: 2019-08-13T08:49:19.096588Z

    location_longitude = fields.FloatField
    location_latitude = fields.FloatField
    location_display_name = fields.CharField(255)
    comment = fields.CharField(255)

    dev_eui = fields.CharField(40, null=False)
    batteryPerc = fields.IntField(null=False) #100,
    configured = fields.BooleanField()
    connTest =   fields.BooleanField()
    deviceType = fields.CharField(255) # "SML Klax",
    meterType = fields.CharField(255) # "SML",
    version = fields.IntField(null=False) #1
    mqtt_topic = fields.CharField(255)

    register0_name = fields.CharField(50)
    register0_Active = fields.BooleanField()
    register0_value = fields.FloatField(default=0.0)
    register0_unit = fields.CharField(5)
    register0_status = fields.IntField()   

    register1_name = fields.CharField(50)
    register1_Active = fields.BooleanField()
    register1_value = fields.FloatField(default=0.0)
    register1_unit = fields.CharField(5)
    register1_status = fields.IntField()  

    register2_name = fields.CharField(50)
    register2_Active = fields.BooleanField()
    register2_value = fields.FloatField(default=0.0)
    register2_unit = fields.CharField(5)
    register2_status = fields.IntField()     

    register3_name = fields.CharField(50)
    register3_Active = fields.BooleanField()
    register3_value = fields.FloatField(default=0.0)
    register3_unit = fields.CharField(5)
    register3_status = fields.IntField()  

    lastseen_at = fields.DatetimeField  #: 2019-08-13T08:49:19.096588Z

    def kWh(self, register_id) -> int:

        kwh: int = -1

        if 0 <= register_id <3:

            if register_id == 0:
                if self.register0_Active:
                    kwh = round(self.register0_value/1000,0)
                    
            elif register_id == 1:
               if self.register1_Active:
                    kwh = round(self.register1_value/1000,0)

            elif register_id == 2:
               if self.register2_Active:
                    kwh = round(self.register2_value/1000,0)

            elif register_id == 3:
               if self.register3_Active:
                    kwh = round(self.register3_value/1000,0)                   
        
        if kwh >= 0:
            return kwh
        else:
            return -1

    def created(self) -> str:
        result = self.inserted_at.strftime(config.DATETIMEFORMAT)
        return result

    def lastseen(self) -> str:
        result = utc2local(self.lastseen_at, config.TIMEZONE).strftime(config.DATETIMEFORMAT)
        return result
    
    def availability(self) -> dict:
        
        duration = self.lastseen_at - self.inserted_at
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]

        percent = round(self._ticks/hours * 100, 0)

        if percent >= 90:
            label = 'success'
            if percent > 100:
                percent = 100
        elif percent > 50:
            label = 'warning'
        else:
            label = 'danger'

        overallavailability = {'percent': percent, 'label': label}

        return overallavailability    

    @property
    def ticks(self) -> int:
        return self._ticks

    @ticks.setter
    def ticks(self, value: int):
        self._ticks = value

    class Meta:
        table = "devices"
        unique_together=("backend_id", "device_extern_id")         

    class PydanticMeta:
        computed = ("kWh", "created", "lastseen", "availability")
        exclude = ("ticks")

Device_Pydantic = pydantic_model_creator(Device, name='Device')
DeviceIn_Pydantic = pydantic_model_creator(Device, name='DeviceIn', exclude_readonly=True)


# Readings
class Measurement(Model):

    id = fields.IntField(pk=True)
    device = fields.ForeignKeyField("models.Device","Measurements", to_field="device_id")
    received_at = fields.DatetimeField()  # 2019-06-24T20:48:09.167897Z,    
    register_id = fields.IntField()
    measurement_nr  = fields.IntField()

    value = fields.FloatField(default=0.0)
    unit = fields.CharField(5, null = False)
    status = fields.IntField(null=False)

    class Meta:
        table = "measurements"
        unique_together=("device_id", "received_at","register_id","measurement_nr")

Measurement_Pydantic = pydantic_model_creator(Measurement, name='Meterreading')


#Loadprofiles
class Loadprofile(Model):

    id = fields.IntField(pk=True)

    device = fields.ForeignKeyField("models.Device","Timeseries", to_field="device_id")
    register_id = fields.IntField()
    start_at = fields.DatetimeField()

    consumption = fields.FloatField(default=0.0)
    meterreading = fields.FloatField(default=0.0)
    unit = fields.CharField(5, null = False)
    status = fields.IntField(null=False)

    class Meta:
        table = "timeseries"
        unique_together=("device_id","register_id", "start_at")

Consumption_Pydantic = pydantic_model_creator(Loadprofile, name='Consumption')
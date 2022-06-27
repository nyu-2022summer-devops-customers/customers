# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
from datetime import date
from factory.fuzzy import FuzzyChoice, FuzzyDate
import factory
from service.models import AddressModel, CustomerModel, Gender


class CustomerFactory(factory.Factory):
    """Creates a customer"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = CustomerModel

    customer_id = factory.Sequence(lambda n: n)
    password = factory.Faker("password", length=63)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    nickname = factory.Faker("name")
    email = factory.LazyAttributeSequence(lambda o, n: '%s@s%d.example.com' % (o.nickname, n))
    gender = FuzzyChoice(choices=[Gender.MALE, Gender.FEMALE, Gender.UNKNOWN])
    birthday = FuzzyDate(date(2008, 1, 1))


class AddressFactory(factory.Factory):
    """Creates an address"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = AddressModel

    customer_id = None
    address_id = factory.Sequence(lambda n: n)
    address = factory.Faker("address")
    
    


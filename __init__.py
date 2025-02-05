"""
Plot stores time series data. This is information that varies with time. We call the data at one instant in time a 'Reading'. Readings take a number of formats depending on the source elements. 

All Readings consist of a date-time and some values. If the measured source has a spread element the Reading will consist of an interval of time.

Instant: This is a single number that represents a value at a particular time. The Reading consists of a date-time and a value at that precise time. Temperature Readings might be recorded using the Reading type instant.

Counter: This is a single accumulated number that counts discrete events. The Reading consists of a date-time and a value. Normally the value increases monotonically, or is static, from one Reading to the next. An example of a counter that is common in everyday life is an odometer in a car."""

__version__ = '4.0.0'

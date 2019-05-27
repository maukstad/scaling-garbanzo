#!/home/mauks/Documents/kerbal/bin/python3

import krpc, time

#connect to server and active ship
conn = krpc.connect(name='subOrbFlight')
vessel = conn.space_center.active_vessel

#set auto pilot and throttle
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()
vessel.control.throttle = 1
time.sleep(1)

#launch
print('Launch')
vessel.control.activate_next_stage()

#ss fuel stage booster sep
fuel_amount = conn.get_call(vessel.resources.amount, 'SolidFuel')
expr = conn.krpc.Expression.less_than(
        conn.krpc.Expression.call(fuel_amount),
        conn.krpc.Expression.constant_float(0.1))

event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Booster separation')
vessel.control.activate_next_stage()

#orbit
mean_altitude = conn.get_call(getattr, vessel.flight(), 'mean_altitude')
expr = conn.krpc.Expression.greater_than(
        conn.krpc.Expression.call(mean_altitude),
        conn.krpc.Expression.constant_double(10000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Gravit turn')
vessel.auto_pilot.target_pitch_and_heading(60, 90)

apoapsis_altitude = conn.get_call(getattr, vessel.orbit, 'apoapsis_altitude')
expr = conn.krpc.Expression.greater_than(
        conn.krpc.Expression.call(apoapsis_altitude),
        conn.krpc.Expression.constant_double(100000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

print('Launch stage separation')
vessel.control.throttle = 0
time.sleep(1)
vessel.control.activate_next_stage()
vessel.auto_pilot.disengage()

#return to kerbin
srf_altitude = conn.get_call(getattr, vessel.flight(), 'surface_altitude')
expr = conn.krpc.Expression.less_than(
        conn.krpc.Expression.call(srf_altitude),
        conn.krpc.Expression.constant_double(3000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()

vessel.control.activate_next_stage()

while vessel.flight(vessel.orbit.body.reference_frame).vertical_speed < -0.1:
    print('Altitude = %.1f meters' % vessel.flight().surface_altitude)
    time.sleep(1)
print('Landed!')



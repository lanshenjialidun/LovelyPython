try:
    code_block()
    #...
except SomeException, e:
    do_some_thing_with_exception(e)
except (Exception1, Exception2), e:
    do_some_thing_with_exception(e)
except:
    do_some_thing_with_other_exceptions()
else:
    do_some_thing_when_success()
finally:
    do_some_thing()
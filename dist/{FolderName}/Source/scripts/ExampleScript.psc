ScriptName ExampleScript Extends ObjectReference

Bool bToggle

Event OnActivate(ObjectReference akActionRef)
	bToggle = !bToggle ; Set Bool to whatever it's not
	If bToggle ; True
		; Do stuff
	Else ; False
		; Undo stuff
	Endif
EndEvent

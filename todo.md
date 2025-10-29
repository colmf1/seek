### TODO:: 

There's a lot we can do in uv 
I'll need 
- shell script to run it should be fine 
- cli app with typer
- need to compile into single binary with uv build 

Currently the nvim output isn't opening correctly 
- Could be due to filename that comes from LLM - it's been looking sus 
- Could be due to being unable to open correct file 
- Should be fixed by shell script 

- Seek set changes provider
- Seek uninstall removes install script  - bash not python

- In two minds - should I have python handle everything or do half it in bash 
- I think bash is better


I think this whole thing was a mistake and I should have done it in python from the start
The reason I want it to be bash is so it works with different shells 
- but python can do that too with os.environ
How? 
- use os.environ to get shell type
- then use subprocess to run the correct commands for that shell:

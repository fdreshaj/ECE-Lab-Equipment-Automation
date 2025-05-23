import pyvisa as visa

def detect_power_supply():
    
    rm = visa.ResourceManager('')
    resources = rm.list_resources()
    print(f"Available resources: {resources}")
    
    for resource in resources:
        print(f"\nTesting {resource}...")
        try:
            # Open the resource
            inst = rm.open_resource(resource)
             
            inst.timeout = 1000  # 1 second timeout
            
            # Try to get instrument ID
            idn = inst.query('*IDN?')
            print(f"SUCCESS - Found instrument on {resource}")
            print(f"Identification: {idn.strip()}")
            
            if 'E36312A' in idn:
                print(f"*** THIS IS YOUR KEYSIGHT E36312A POWER SUPPLY ***")
                print(f"Connection established to: '{resource}'")

                # Keep the connection open for multiple commands
                while True:
                    print("\n--- Power Supply Control Options ---")
                    print(" 'on'     : Turn ON a channel output")
                    print(" 'off'    : Turn OFF a channel output")
                    print(" 'status' : Check a channel's output status")
                    print(" 'voltage': Set Voltage for a channel")
                    print(" 'exit'   : Disconnect and exit")
                    
                    userInput = input("Enter command: ").lower().strip()

                    if userInput in ['on', 'off', 'status', 'voltage']:
                        while True:
                            try:
                                channel_input = input("Enter channel number (1, 2, or 3): ").strip()
                                channel = int(channel_input)
                                if channel not in [1, 2, 3]:
                                    raise ValueError("Channel number must be 1, 2, or 3.")
                                break # Exit channel input loop if valid
                            except ValueError as e:
                                print(f"Invalid channel number: {e}")
                                
                        if userInput == 'off':
                            inst.write(f'OUTPut:STATe OFF, (@{channel})')
                            print(f"Channel {channel} is now OFF.")
                        elif userInput == 'on':
                            inst.write(f'OUTPut:STATe ON, (@{channel})')
                            print(f"Channel {channel} is now ON.")
                        elif userInput == 'status':
                            status = inst.query(f'OUTPut:STATe? (@{channel})').strip()
                            if status == '1':
                                print(f"Channel {channel} output is currently ON.")
                            elif status == '0':
                                print(f"Channel {channel} output is currently OFF.")
                            else:
                                print(f"Unrecognized status for Channel {channel}: {status}")
                        elif userInput == 'voltage':
                            while True:
                                try:
                                    voltage_str = input(f"Enter desired voltage for Channel {channel} (e.g., 5.0, 12.5): ").strip()
                                    voltage = float(voltage_str)
                                    
                                    inst.write(f'SOURce:VOLTage {voltage}, (@{channel})')
                                    print(f"Channel {channel} voltage set to {voltage} V.")
                                    break 
                                except ValueError:
                                    print("Invalid voltage. Please enter a numerical value.")
                                except Exception as e:
                                    print(f"Error setting voltage: {e}")
                                    break # Exit if there's an instrument error
                    elif userInput == 'exit':
                        print("Exiting control. Disconnecting from power supply.")
                        inst.close()
                        break 
                    else:    
                        print("Invalid command. Please try again.")
            
        except Exception as e:
            print(f"No response from {resource}: {e}")
    
    rm.close() 
    print("\nDetection complete!")

if __name__ == "__main__":
    detect_power_supply()
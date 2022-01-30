# -*- coding: utf-8 -*-
import csv
import time

'''start function file io'''
def get_params_from_csv(param_file_dir):
    with open(param_file_dir) as config_file:
        param_list = csv.reader(config_file)
        param_list = [row for row in param_list]

        '''このゴミコードどうにかしたい'''
        return(int(param_list[0][1]),float(param_list[1][1]),float(param_list[2][1]),float(param_list[3][1]),float(param_list[4][1]),float(param_list[5][1]),float(param_list[6][1]),float(param_list[7][1]),int(param_list[8][1]),float(param_list[9][1]),float(param_list[10][1]))

def set_output_csv():
    with open('sbsim_energy_output.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['quake_number','quake_energy'])

def output_quake_energy_to_csv(int,energy,energy_before,energy_after):
    with open('sbsim_energy_output.csv', 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([str(int),energy,energy_before,energy_after])
'''end function file io'''

'''start grobal params'''
#imput params
param_file_dir = 'sbsim_config.csv'
(how_many_springs,block_mass,block_length,spring_length,gravity,spring_const,static_friction,dynamic_friction,quake_howmany,pull_1st_block_range,quake_sim_dt) = get_params_from_csv(param_file_dir)
'''end grobal params'''

'''start main function'''
def main():
    #set output file
    set_output_csv()

    #set coordinations
    coordinations = [float(0)] * (how_many_springs+1)
    for i in range(how_many_springs):
        coordinations[i+1] = coordinations[i] - block_length - spring_length
    
    #start simulator
    for i in range(quake_howmany):
        #pull blocks while quake happens
        while(is_1st_blocks_move(coordinations)==False):
            coordinations[0] += pull_1st_block_range
        energy_before = calc_energy(coordinations)
        coordinations = sim_quake(coordinations)
        energy_after = calc_energy(coordinations)
        output_quake_energy_to_csv(i+1,energy_before - energy_after,energy_before,energy_after)
    

'''end main function'''

'''start function simulation'''
def calc_energy(coordinations):
    sigma_square_energy = 0
    for i in range(how_many_springs):
        sigma_square_energy += pow(coordinations[i] - coordinations[i+1] - block_length - spring_length,2)
    return(sigma_square_energy * 0.5 * spring_const)

def is_1st_blocks_move(coordinations):
    if(abs(coordinations[0]-2*coordinations[1]+coordinations[2])*spring_const<=static_friction*block_mass*gravity):
        return(False)
    else:
        return(True)

def check_zero(arr):
    for i in range(len(arr)):
        if arr[i] != 0:
            return False
    return True

def calc_spring_force(coordinations,block,lr):
    if(lr == 'r'):
        if(block == how_many_springs):
            stretch_length = 0  #rightest block has no spring on the right
        else:
            stretch_length = coordinations[block]-coordinations[block+1] -spring_length - block_length
    elif(lr == 'l'):
        stretch_length = coordinations[block-1]-coordinations[block] -spring_length - block_length
    return(stretch_length*spring_const)

def sim_quake(coordinations):
    acc = [float(0)] * (how_many_springs+1)
    v_new = [float(1)] * (how_many_springs+1)
    v_old = [float(0)] * (how_many_springs+1)
    #while (check_zero(v_new)==False) or (check_zero(v_old)==False):
    for j in range(int(1/quake_sim_dt)):
        #calc acc
        for i in range(1,how_many_springs+1):
            join_spring_forces = calc_spring_force(coordinations,i,'l') - calc_spring_force(coordinations,i,'r')
            if(v_old[i]>0):
                acc[i] = join_spring_forces - block_mass*gravity*dynamic_friction
                acc[i] /= block_mass
            elif(v_old[i]<0):
                acc[i] = join_spring_forces + block_mass*gravity*dynamic_friction
                acc[i] /= block_mass
            else:
                if(abs(join_spring_forces) <= block_mass*gravity*static_friction):
                    acc[i] = 0
                elif (join_spring_forces > 0):
                    acc[i] = join_spring_forces - block_mass*gravity*static_friction
                    acc[i] /= block_mass
                else:
                    acc[i] = join_spring_forces + block_mass*gravity*static_friction
                    acc[i] /= block_mass
        #calc v_new
        for i in range(1,how_many_springs+1):
            v_new[i] = v_old[i] + quake_sim_dt*acc[i]
        #If v_new crosses 0 from v_old, set v_new to 0
        for i in range(1,how_many_springs+1):
            if (v_new[i] * v_old[i] < 0):
                v_new[i] = 0
        #calc coordination
        for i in range(1,how_many_springs+1):
            coordinations[i] += quake_sim_dt*v_new[i]
        #clear v_new
        for i in range(1,how_many_springs+1):
            v_old[i] = v_new[i]
            v_new[i] = 0
    return(coordinations)
'''end function simulation'''


if __name__ == "__main__":
    start_time = time.time()
    main()
    print('it took ' + str(time.time()-start_time) + ' seconds')
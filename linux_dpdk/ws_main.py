#!/usr/bin/env python
# encoding: utf-8

#
# Hanoh Haim
# Cisco Systems, Inc.



VERSION='0.0.1'
APPNAME='cxx_test'
import os;
import commands;
import shutil;
import copy;
import re


# these variables are mandatory ('/' are converted automatically)
top = '../'
out = 'build_dpdk'


b_path ="./build/linux_dpdk/"

#######################################
# utility for group source code 
###################################

class SrcGroup:
    ' group of source by directory '

    def __init__(self,dir,src_list):
      self.dir = dir;
      self.src_list = src_list;
      self.group_list = None;
      assert (type(src_list)==list)
      assert (type(dir)==str)



    def file_list (self,top):
        ' return  the long list of the files '
        res=''
        for file in self.src_list:
            res= res + top+'/'+self.dir+'/'+file+'  ';
        return res;

    def __str__ (self):
        return (self.file_list(''));

    def __repr__ (self):
        return (self.file_list(''));



class SrcGroups:
    ' group of source groups '

    def __init__(self,list_group):
      self.list_group = list_group;
      assert (type(list_group)==list)


    def file_list (self,top):
          ' return  the long list of the files '
          res=''
          for o in self.list_group:
              res += o.file_list(top);
          return res;


    def __str__ (self):
          return (self.file_list(''));

    def __repr__ (self):
          return (self.file_list(''));


#######################################




#I put v3 as v4 contain temp fix for falcon

def options(opt):
    opt.load('compiler_cxx')
    opt.load('compiler_cc')

def configure(conf):
    conf.load('g++')
    conf.load('gcc')


main_src = SrcGroup(dir='src',
        src_list=[
             'utl_term_io.cpp',
             'global_io_mode.cpp',
             'main_dpdk.cpp',
             'bp_sim.cpp',
             'platform_cfg.cpp',
             'tuple_gen.cpp',
             'rx_check.cpp',
             'rx_check_header.cpp',
             'timer_wheel_pq.cpp',
             'time_histogram.cpp',
             'os_time.cpp',
             'utl_cpuu.cpp',
             'utl_json.cpp',
             'utl_yaml.cpp',
             'nat_check.cpp',
             'msg_manager.cpp',
             'pal/linux_dpdk/pal_utl.cpp',
             'pal/linux_dpdk/mbuf.cpp'
             ]);

cmn_src = SrcGroup(dir='src/common',
    src_list=[ 
        'basic_utils.cpp',
        'captureFile.cpp',
        'erf.cpp',
        'pcap.cpp',
        ]);

         

# CFT core files
net_src = SrcGroup(dir='src/common/Network/Packet',
        src_list=[
           'CPktCmn.cpp',
           'EthernetHeader.cpp',
           'IPHeader.cpp',
           'TCPHeader.cpp',
           'TCPOptions.cpp',
           'UDPHeader.cpp',
           'MacAddress.cpp',
           'VLANHeader.cpp']);

yaml_src = SrcGroup(dir='yaml-cpp/src/',
        src_list=[
            'aliasmanager.cpp',
            'binary.cpp',
            'contrib/graphbuilder.cpp',
            'contrib/graphbuilderadapter.cpp',
            'conversion.cpp',
            'directives.cpp',
            'emitfromevents.cpp',
            'emitter.cpp',
            'emitterstate.cpp',
            'emitterutils.cpp',
            'exp.cpp',
            'iterator.cpp',
            'node.cpp',
            'nodebuilder.cpp',
            'nodeownership.cpp',
            'null.cpp',
            'ostream.cpp',
            'parser.cpp',
            'regex.cpp',
            'scanner.cpp',
            'scanscalar.cpp',
            'scantag.cpp',
            'scantoken.cpp',
            'simplekey.cpp',
            'singledocparser.cpp',
            'stream.cpp',
            'tag.cpp']);

dpdk_src = SrcGroup(dir='src/dpdk_lib18/',
                src_list=[
                 'librte_ring/rte_ring.c',
                 'librte_timer/rte_timer.c',


                #'librte_pmd_ixgbe/ixgbe_82599_bypass.c',
                #'librte_pmd_ixgbe/ixgbe_bypass.c',
                'librte_pmd_ixgbe/ixgbe_ethdev.c',
                'librte_pmd_ixgbe/ixgbe_fdir.c',
                'librte_pmd_ixgbe/ixgbe_pf.c',
                'librte_pmd_ixgbe/ixgbe_rxtx.c',
                'librte_pmd_ixgbe/ixgbe_rxtx_vec.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_82598.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_82599.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_api.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_common.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_dcb.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_dcb_82598.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_dcb_82599.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_mbx.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_phy.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_vf.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_x540.c',
                'librte_pmd_ixgbe/ixgbe/ixgbe_x550.c',

                'librte_pmd_vmxnet3/vmxnet3_ethdev.c',
                'librte_pmd_vmxnet3/vmxnet3_rxtx.c',

                'librte_pmd_virtio/virtio_ethdev.c',
                'librte_pmd_virtio/virtio_pci.c',
                'librte_pmd_virtio/virtio_rxtx.c',
                'librte_pmd_virtio/virtqueue.c',

                'librte_pmd_enic/enic_clsf.c',
                'librte_pmd_enic/enic_ethdev.c',
                'librte_pmd_enic/enic_main.c',
                'librte_pmd_enic/enic_res.c',
                'librte_pmd_enic/vnic/vnic_cq.c',
                'librte_pmd_enic/vnic/vnic_dev.c',
                'librte_pmd_enic/vnic/vnic_intr.c',
                'librte_pmd_enic/vnic/vnic_rq.c',
                'librte_pmd_enic/vnic/vnic_rss.c',
                'librte_pmd_enic/vnic/vnic_wq.c',

                 'librte_malloc/malloc_elem.c',
                 'librte_malloc/malloc_heap.c',
                 'librte_malloc/rte_malloc.c',

                 'librte_mbuf/rte_mbuf.c',
                 'librte_mempool/rte_mempool.c',

                 'librte_pmd_e1000/em_ethdev.c',
                 'librte_pmd_e1000/em_rxtx.c',
                 'librte_pmd_e1000/igb_ethdev.c',
                 'librte_pmd_e1000/igb_pf.c',
                 'librte_pmd_e1000/igb_rxtx.c',
                 'librte_pmd_e1000/e1000/e1000_80003es2lan.c',
                 'librte_pmd_e1000/e1000/e1000_82540.c',
                 'librte_pmd_e1000/e1000/e1000_82541.c',
                 'librte_pmd_e1000/e1000/e1000_82542.c',
                 'librte_pmd_e1000/e1000/e1000_82543.c',
                 'librte_pmd_e1000/e1000/e1000_82571.c',
                 'librte_pmd_e1000/e1000/e1000_82575.c',
                 'librte_pmd_e1000/e1000/e1000_api.c',
                 'librte_pmd_e1000/e1000/e1000_i210.c',
                 'librte_pmd_e1000/e1000/e1000_ich8lan.c',
                 'librte_pmd_e1000/e1000/e1000_mac.c',
                 'librte_pmd_e1000/e1000/e1000_manage.c',
                 'librte_pmd_e1000/e1000/e1000_mbx.c',
                 'librte_pmd_e1000/e1000/e1000_nvm.c',
                 'librte_pmd_e1000/e1000/e1000_osdep.c',
                 'librte_pmd_e1000/e1000/e1000_phy.c',
                 'librte_pmd_e1000/e1000/e1000_vf.c',
                 'librte_hash/rte_fbk_hash.c',
                 'librte_hash/rte_hash.c',
                 'librte_cmdline/cmdline.c',
                 'librte_cmdline/cmdline_cirbuf.c',
                 'librte_cmdline/cmdline_parse.c',
                 'librte_cmdline/cmdline_parse_etheraddr.c',
                 'librte_cmdline/cmdline_parse_ipaddr.c',
                 'librte_cmdline/cmdline_parse_num.c',
                 'librte_cmdline/cmdline_parse_portlist.c',
                 'librte_cmdline/cmdline_parse_string.c',
                 'librte_cmdline/cmdline_rdline.c',
                 'librte_cmdline/cmdline_socket.c',
                 'librte_cmdline/cmdline_vt100.c',

            'librte_eal/common/eal_common_cpuflags.c',
            'librte_eal/common/eal_common_dev.c',
            'librte_eal/common/eal_common_devargs.c',
            'librte_eal/common/eal_common_errno.c',
            'librte_eal/common/eal_common_hexdump.c',
            'librte_eal/common/eal_common_launch.c',
            'librte_eal/common/eal_common_log.c',
            'librte_eal/common/eal_common_memory.c',
            'librte_eal/common/eal_common_memzone.c',
            'librte_eal/common/eal_common_options.c',
            'librte_eal/common/eal_common_pci.c',
            'librte_eal/common/eal_common_string_fns.c',
            'librte_eal/common/eal_common_tailqs.c',

            'librte_ether/rte_ethdev.c',

            'librte_pmd_ring/rte_eth_ring.c',
            'librte_kvargs/rte_kvargs.c',


            'librte_eal/linuxapp/eal/eal.c',
            'librte_eal/linuxapp/eal/eal_alarm.c',
            'librte_eal/linuxapp/eal/eal_debug.c',
            'librte_eal/linuxapp/eal/eal_hugepage_info.c',
            'librte_eal/linuxapp/eal/eal_interrupts.c',
            'librte_eal/linuxapp/eal/eal_ivshmem.c',
            'librte_eal/linuxapp/eal/eal_lcore.c',
            'librte_eal/linuxapp/eal/eal_log.c',
            'librte_eal/linuxapp/eal/eal_memory.c',
            'librte_eal/linuxapp/eal/eal_pci.c',
            'librte_eal/linuxapp/eal/eal_pci_uio.c',
            'librte_eal/linuxapp/eal/eal_pci_vfio.c',
            'librte_eal/linuxapp/eal/eal_pci_vfio_mp_sync.c',
            'librte_eal/linuxapp/eal/eal_thread.c',
            'librte_eal/linuxapp/eal/eal_timer.c',
            #'librte_eal/linuxapp/eal/eal_xen_memory.c'

            'librte_pmd_i40e/i40e_ethdev.c',
            'librte_pmd_i40e/i40e_ethdev_vf.c',
            'librte_pmd_i40e/i40e_fdir.c',
            'librte_pmd_i40e/i40e_pf.c',
            'librte_pmd_i40e/i40e_rxtx.c',
            'librte_pmd_i40e/i40e/i40e_adminq.c',
            'librte_pmd_i40e/i40e/i40e_common.c',
            'librte_pmd_i40e/i40e/i40e_dcb.c',
            'librte_pmd_i40e/i40e/i40e_diag.c',
            'librte_pmd_i40e/i40e/i40e_hmc.c',
            'librte_pmd_i40e/i40e/i40e_lan_hmc.c',
            'librte_pmd_i40e/i40e/i40e_nvm.c'
            ]);




bp_dpdk =SrcGroups([
                dpdk_src
                ]);



# this is the library dp going to falcon (and maybe other platforms)
bp =SrcGroups([
                main_src, 
                cmn_src ,
                net_src ,
                yaml_src,
                #sw_mini_shell_grp_src
                #dpdk_src
                ]);

l2fwd_main_src = SrcGroup(dir='src',
        src_list=[
             'l2fwd/main.c'
             ]);


l2fwd =SrcGroups([
                l2fwd_main_src]);



cxxflags_base =['-DWIN_UCODE_SIM',
           '-D_BYTE_ORDER',
           '-Wno-format',
           '-D_LITTLE_ENDIAN',
           '-DLINUX',
           '-g',
           '-DRTE_DPDK',
           '-march=native',
           '-DRTE_MACHINE_CPUFLAG_SSE',
           '-DRTE_MACHINE_CPUFLAG_SSE2',
           '-DRTE_MACHINE_CPUFLAG_SSE3',
           '-DRTE_MACHINE_CPUFLAG_SSSE3',
           '-DRTE_MACHINE_CPUFLAG_SSE4_1',
           '-DRTE_MACHINE_CPUFLAG_SSE4_2',
           '-DRTE_MACHINE_CPUFLAG_AES',
           '-DRTE_MACHINE_CPUFLAG_PCLMULQDQ',
           '-DRTE_MACHINE_CPUFLAG_AVX',
           '-DRTE_COMPILE_TIME_CPUFLAGS=RTE_CPUFLAG_SSE3,RTE_CPUFLAG_SSE,RTE_CPUFLAG_SSE2,RTE_CPUFLAG_SSSE3,RTE_CPUFLAG_SSE4_1,RTE_CPUFLAG_SSE4_2,RTE_CPUFLAG_AES,RTE_CPUFLAG_PCLMULQDQ,RTE_CPUFLAG_AVX',
           '-include','../src/pal/linux_dpdk/dpdk180/rte_config.h'
       ];

cxxflags_base_old =['-DWIN_UCODE_SIM',
           '-D_BYTE_ORDER',
           '-D_LITTLE_ENDIAN',
           '-DLINUX',
           '-Wno-format',
           '-DUCS_210',
           '-g',
           '-DRTE_DPDK',
           '-march=corei7',
           '-mtune=generic',
           '-DRTE_MACHINE_CPUFLAG_SSE',
           '-DRTE_COMPILE_TIME_CPUFLAGS=RTE_CPUFLAG_SSE',
           '-include','../src/pal/linux_dpdk/dpdk180/rte_config.h'
       ];




includes_path =''' ../src/pal/linux_dpdk/
                   ../src/
                   ../yaml-cpp/include/
                   ../src/zmq/include/
                        ../src/dpdk_lib18/librte_eal/linuxapp/eal/include/
                        ../src/dpdk_lib18/librte_eal/common/include/
                        ../src/dpdk_lib18/librte_eal/common/
                        ../src/dpdk_lib18/librte_eal/common/include/arch/x86

                        ../src/dpdk_lib18/librte_ring/
                        ../src/dpdk_lib18/librte_mempool/
                        ../src/dpdk_lib18/librte_malloc/
                        ../src/dpdk_lib18/librte_ether/

                        ../src/dpdk_lib18/librte_cmdline/
                        ../src/dpdk_lib18/librte_hash/
                        ../src/dpdk_lib18/librte_lpm/
                        ../src/dpdk_lib18/librte_mbuf/
                        ../src/dpdk_lib18/librte_pmd_igb/
                        ../src/dpdk_lib18/librte_pmd_ixgbe/

                        ../src/dpdk_lib18/librte_pmd_enic/
                        ../src/dpdk_lib18/librte_pmd_enic/vnic/
                        ../src/dpdk_lib18/librte_pmd_virtio/
                        ../src/dpdk_lib18/librte_pmd_vmxnet3/

                        ../src/dpdk_lib18/librte_timer/
                        ../src/dpdk_lib18/librte_net/
                        ../src/dpdk_lib18/librte_pmd_ring/
                        ../src/dpdk_lib18/librte_kvargs/


              ''';

dpdk_includes_path =''' ../src/ 
                        ../src/pal/linux_dpdk/
                        ../src/dpdk_lib18/librte_eal/linuxapp/eal/include/
                        ../src/dpdk_lib18/librte_eal/common/include/
                        ../src/dpdk_lib18/librte_eal/common/
                        ../src/dpdk_lib18/librte_eal/common/include/arch/x86

                        ../src/dpdk_lib18/librte_pmd_enic/
                        ../src/dpdk_lib18/librte_pmd_virtio/
                        ../src/dpdk_lib18/librte_pmd_vmxnet3/
                        ../src/dpdk_lib18/librte_pmd_enic/vnic/

                        ../src/dpdk_lib18/librte_ring/
                        ../src/dpdk_lib18/librte_mempool/
                        ../src/dpdk_lib18/librte_malloc/
                        ../src/dpdk_lib18/librte_ether/
                        ../src/dpdk_lib18/librte_cmdline/
                        ../src/dpdk_lib18/librte_hash/
                        ../src/dpdk_lib18/librte_lpm/
                        ../src/dpdk_lib18/librte_mbuf/
                        ../src/dpdk_lib18/librte_pmd_igb/
                        ../src/dpdk_lib18/librte_pmd_ixgbe/
                        ../src/dpdk_lib18/librte_timer/
                        ../src/dpdk_lib18/librte_net/
                        ../src/dpdk_lib18/librte_pmd_ring/
                        ../src/dpdk_lib18/librte_kvargs/

                    ''';


DPDK_WARNING=['-D_GNU_SOURCE'];




RELEASE_    = "release"
DEBUG_      = "debug"
PLATFORM_64 = "64"
PLATFORM_32 = "32"


class build_option:

    def __init__(self,platform,debug_mode,is_pie):
      self.mode     = debug_mode;   ##debug,release
      self.platform = platform; #['32','64'] 
      self.is_pie = is_pie

    def __str__(self):
       s=self.mode+","+self.platform;
       return (s);

    def lib_name(self,lib_name_p,full_path):
        if full_path:
            return b_path+lib_name_p;
        else:
            return lib_name_p;
    #private functions
    def toLib (self,name,full_path = True):
        lib_n = "lib"+name+".a";
        return (self.lib_name(lib_n,full_path));

    def toExe(self,name,full_path = True):
        return (self.lib_name(name,full_path));

    def is64Platform (self):
        return ( self.platform == PLATFORM_64);

    def isRelease (self):
        return ( self.mode  == RELEASE_);
     
    def isPIE (self):
        return self.is_pie
    
    def update_executable_name (self,name):
        return self.update_name(name,"-")

    def update_non_exe_name (self,name):
        return self.update_name(name,"_")

    def update_name (self,name,delimiter):
        trg = copy.copy(name);
        if self.is64Platform():
            trg += delimiter + "64";
        else:
            trg += delimiter + "32";

        if self.isRelease () :
            trg += "";
        else:
            trg +=  delimiter + "debug";

        if self.isPIE():
            trg += delimiter + "o"
        return trg;

    def cxxcomp_flags (self,flags):
        result = copy.copy(flags);
        if self.is64Platform () :
            result+=['-m64'];
        else:
            result+=['-m32'];

        if self.isRelease () :
            result+=['-O3'];
        else:
            result+=['-O0'];#'-DDEBUG','-D_DEBUG','-DSTILE_CPP_ASSERT','-DSTILE_SHIM_ASSERT'

        return result;

    # handles shim options
    def get_target_shim (self):
        trg = "mcpshim";
        return self.update_non_exe_name(trg);

    def get_flags_shim (self):
        flags = ['-DWIN_UCODE_SIM', '-DLINUX' ,'-g'];
        return self.cxxcomp_flags(flags);


    def get_lib_shim(self,full_path = True):
        return self.toLib(self.get_target_shim(),full_path);

    def shim_print (self):
        print "\tshim: target name is "+self.get_target_shim();
        print "\tshim: compile flags are "+str(self.get_flags_shim());
        print "\tshim: lib full pathname is " +self.get_lib_shim();
        print "\n";

    # handle falcon stub options
    def get_target_falcon_stub (self):
        trg = "falcon_stub";
        return self.update_non_exe_name(trg);

    def get_flags_falcon_stub (self):
        return self.cxxcomp_flags(cxxflags_base);

    def get_lib_falcon_stub (self):
        return self.toLib(self.get_target_falcon_stub());

    def falcon_stub_print (self):
        
        print "\tfalcon_stub: target name is "+self.get_target_falcon_stub();
        print "\tfalcon_stub: compile flags are "+str(self.get_flags_falcon_stub());
        print "\tfalcon_stub: lib full pathname is " +self.get_lib_falcon_stub();
        print "\n";

    # handle stile-dp options
    def get_target_stile_dp (self):
        trg = "stile_dp";
        return self.update_non_exe_name(trg);

    def get_flags_stile_dp (self):
        return self.cxxcomp_flags(cxxflags_base);

    def get_lib_stile_dp(self, full_path = True):
        return self.toLib(self.get_target_stile_dp(),full_path);

    def stile_dp_print (self):
       
        print "\tstile_dp: target name is "+self.get_target_stile_dp();
        print "\tstile_dp: compile flags are "+str(self.get_flags_stile_dp());
        print "\tstile_dp: lib full pathname is " +self.get_lib_stile_dp();
        print "\n";

    # handle stile-away main program options
    def get_target (self):
        return self.update_executable_name("_t-rex");

    def get_target_l2fwd (self):
        return self.update_executable_name("l2fwd");

    def get_dpdk_target (self):
        return self.update_executable_name("dpdk");

    def get_flags (self):
        if self.isPIE():
            return self.cxxcomp_flags(cxxflags_base_old);
        else:
            return self.cxxcomp_flags(cxxflags_base);



    def get_link_flags(self):
        # add here basic flags
        base_flags = ['-L/lib64', '-lpthread','-ldl'];
        #if self.isPIE():
        #    base_flags.append('-lstdc++')

        #platform depended flags

        if self.is64Platform():
            base_flags += ['-m64'];
        else:
            base_flags += ['-lrt'];

        return base_flags;

    def get_exe (self,full_path = True):
        return self.toExe(self.get_target(),full_path);

    def stileaway_print (self):
       
        print "\ttarget name is "+self.get_target();
        print "\tcompile flags are "+str(self.get_flags());
        print "\tlink flags are " + str(self.get_link_flags());
        print "\texe full pathname is " +self.get_exe();
        print "\n";

    # handle pi options
    def get_target_pi(self):
        if self.is64Platform():
            return "stile64";
        else:
            return "stile32";
        
    def get_lib_pi_path(self):

        if self.is64Platform():
            return cntrl_lib64bit_path;
        else:
            return cntrl_lib32bit_path;

    def get_lib_pi(self,full_path = True):
        lib_name_p = "lib"+self.get_target_pi()+".a"
        if full_path:
            return self.get_lib_pi_path() + lib_name_p;
        else:
            return lib_name_p;

    def stile_pi_print(self):

        print "\tstile_cp: target name is " + self.get_target_pi();
        print "\tstile_cp: lib full pathname is " +self.get_lib_pi();
        print "\n";


    def get_target_stile_cp (self):
         if self.is64Platform():
            cp = "stile_cp_64";
         else:
            cp = "stile_cp_32";
	 
	 return cp

    # handle release options

    def get_flags_release(self):
        return self.cxxcomp_flags(cxxflags_base);

    def get_release_link_flags(self,include_lib=True):
        # add here basic flags
        base_flags = ['-lpthread'];
        #if self.isPIE():
        #   base_flags += ['-lstdc++']

        if include_lib:
            #those are the linked libraries
            base_flags += ["-L"+release_lib,
                           "-l"+self.get_target_stile_dp(),
                           "-l"+self.get_target_stile_cp(),
                           "-l"+self.get_target_shim(),
                           "-l"+self.get_target_falcon_stub(),
                           ];

        #platform depended flags
        if self.is64Platform():
            base_flags += ['-m64'];
        else:
            base_flags += ['-lrt'];
        return base_flags;

    def get_target_release (self):
        return self.update_non_exe_name("stile-away-pkg");
    def get_target_falcon_test(self):
        return self.update_non_exe_name("stile-away-falcon-stand-alone");

    def release_print(self):

        print "\trelease: target name is " + self.get_target_release();
        print "\trelease: link flags are " + str(self.get_release_link_flags());
        print "\n";
    cp_output_lib   = ['libstile_cp_32.a', 'libstile_cp_64.a', 'libstile_cp_32.a', 'libstile_cp_64.a', 'libstile_cp_64_pie.a'];
    
    def calculate_index (self):
        index = 0;
        if self.isRelease():
           index += 2;
        if self.is64Platform():
            index += 1;
	if self.isPIE():
	    index += 1;
        return index;
    def get_install_cp(self):
        return self.cp_output_lib[self.calculate_index()];


build_types = [
               build_option(debug_mode= DEBUG_, platform = PLATFORM_64, is_pie = False),

               build_option(debug_mode= RELEASE_,platform = PLATFORM_64, is_pie = False),

               build_option(debug_mode= DEBUG_, platform = PLATFORM_64, is_pie = True),
               build_option(debug_mode= RELEASE_,platform = PLATFORM_64, is_pie = True),

              ]



def build_prog (bld, build_obj):

    zmq_lib_path='src/zmq/'
    bld.read_shlib( name='zmq' , paths=[top+zmq_lib_path] )

    #rte_libs =[
    #         'dpdk'];

    #rte_libs1 = rte_libs+rte_libs+rte_libs;

    #for obj in rte_libs:
    #    bld.read_shlib( name=obj , paths=[top+rte_lib_path] )

    bld.objects(
      features='c ',
      includes = dpdk_includes_path,
      
      cflags   = (build_obj.get_flags()+DPDK_WARNING ),
      source   = bp_dpdk.file_list(top),
      target=build_obj.get_dpdk_target() 
      );

    bld.program(features='cxx cxxprogram', 
                includes =includes_path,
                cxxflags =build_obj.get_flags(),
                linkflags = build_obj.get_link_flags() ,
                lib=['pthread','dl'],
                use =[build_obj.get_dpdk_target(),'zmq'],
                source = bp.file_list(top),
                target = build_obj.get_target())



def build_type(bld,build_obj):
    build_prog(bld, build_obj);


def post_build(bld):
    print "copy objects"
    exec_p ="../scripts/"
    for obj in build_types:
        install_single_system(bld, exec_p, obj);

def build(bld):
    bld.add_post_fun(post_build);
    for obj in build_types:
        build_type(bld,obj);


def build_info(bld):
    for obj in build_types:
        print str(obj);
        obj.stileaway_print();


      
def install_single_system (bld, exec_p, build_obj):
    o='build_dpdk/linux_dpdk/';
    src_file =  os.path.realpath(o+build_obj.get_target())
    if os.path.exists(src_file):
        dest_file = exec_p +build_obj.get_target()
        print dest_file
        if not os.path.lexists(dest_file):
            relative_path = os.path.relpath(src_file, exec_p)
            os.symlink(relative_path, dest_file);

#
# need to fix this
def install1(bld):
    print "copy images and libs"
    exec_p ="./"
 
    for obj in build_types:
        install_single_system(bld,exec_p,obj);

def copy_single_system (bld, exec_p, build_obj):
    o='build_dpdk/linux_dpdk/';
    src_file =  os.path.realpath(o+build_obj.get_target())
    print src_file;
    if os.path.exists(src_file):
        dest_file = exec_p +build_obj.get_target()
        print dest_file
        os.system("cp %s %s " %(src_file,dest_file));
        os.system("chmod +x %s " %(dest_file));

def copy_single_system1 (bld, exec_p, build_obj):
    o='../scripts/';
    src_file =  os.path.realpath(o+build_obj.get_target()[1:])
    print src_file;
    if os.path.exists(src_file):
        dest_file = exec_p +build_obj.get_target()[1:]
        os.system("cp %s %s " %(src_file,dest_file));
        os.system("chmod +x %s " %(dest_file));


files_list=[
            'libzmq.so.3.1.0',
            'libzmq.so.3',
            'trex-cfg',
            'bp-sim-32',
            'bp-sim-64',
            'bp-sim-32-debug',
            'bp-sim-64-debug',
            'release_notes.pdf',
            'dpdk_nic_bind.py',
            'dpdk_setup_ports.py',
            'doc_process.py',
            'trex_daemon_server'
            ];

files_dir=['cap2','avl','cfg','ko','automation','python-lib']

RELEASE ='v1.73'

def release(bld):
    print "copy images and libs"
    exec_p ="/auto/proj-pcube-b/apps/PL-b/tools/bp_sim2/"+RELEASE+"/"
    os.system(' mkdir -p '+exec_p);
    
    for obj in build_types:
        copy_single_system (bld,exec_p,obj);
        copy_single_system1 (bld,exec_p,obj)

    for obj in files_list:
        src_file =  '../scripts/'+obj
        dest_file = exec_p +'/'+obj
        os.system("cp %s %s " %(src_file,dest_file));

    for obj in files_dir:
        src_file =  '../scripts/'+obj+'/' 
        dest_file = exec_p +'/'+obj+'/'
        os.system("cp -rv %s %s " %(src_file,dest_file));
        os.system("chmod 755 %s " %(dest_file));

    os.system('cd %s/..;tar --exclude="*.pyc" -zcvf %s/%s.tar.gz %s' %(exec_p,os.getcwd(),RELEASE,RELEASE))
    os.system("mv %s/%s.tar.gz %s" % (os.getcwd(),RELEASE,exec_p));


def publish(bld):

    exec_p ="/auto/proj-pcube-b/apps/PL-b/tools/bp_sim2/"+RELEASE+"/"

    release_name ='%s.tar.gz' % (RELEASE);
    from_        = exec_p+'/'+release_name;
    os.system("rsync -av %s csi-wiki-01:/opt/apache-tomcat-7.0.52/webapps/trex/release/%s " %(from_,release_name))
    os.system("ssh csi-wiki-01 'cd /opt/apache-tomcat-7.0.52/webapps/trex/release/;rm be_latest; ln -P %s be_latest'  " %(release_name))
    os.system("ssh csi-wiki-01 'cd /opt/apache-tomcat-7.0.52/webapps/trex/release/;rm latest; ln -P %s latest'  " %(release_name))

def publish_ext(bld):

    exec_p ="/auto/proj-pcube-b/apps/PL-b/tools/bp_sim2/"+RELEASE+"/"

    release_name ='%s.tar.gz' % (RELEASE);
    from_        = exec_p+'/'+release_name;
    os.system('rsync -avz -e "ssh -i /auto/srg-sce-swinfra-usr/emb/users/hhaim/work/trex-1-keys.pem" --rsync-path=/usr/bin/rsync %s root@trex-tgn.cisco.com:/var/www/html/trex/release/%s' % (from_,release_name) )
    os.system("ssh -i /auto/srg-sce-swinfra-usr/emb/users/hhaim/work/trex-1-keys.pem -l root trex-tgn.cisco.com 'cd /var/www/html/trex/release/;rm be_latest; ln -P %s be_latest'  " %(release_name))
    os.system("ssh -i /auto/srg-sce-swinfra-usr/emb/users/hhaim/work/trex-1-keys.pem -l root trex-tgn.cisco.com 'cd /var/www/html/trex/release/;rm latest; ln -P %s latest'  " %(release_name))












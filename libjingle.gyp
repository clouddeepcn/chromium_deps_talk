#
# libjingle
# Copyright 2012, Google Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#  3. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

{
  'includes': ['build/common.gypi'],
  'conditions': [
    ['os_posix == 1 and OS != "mac" and OS != "ios"', {
     'conditions': [
       ['sysroot!=""', {
         'variables': {
           'pkg-config': '../../../build/linux/pkg-config-wrapper "<(sysroot)" "<(target_arch)"',
         },
       }, {
         'variables': {
           'pkg-config': 'pkg-config'
         },
       }],
     ],
    }],
    ['OS=="linux" or OS=="android"', {
      'targets': [
        {
          'target_name': 'libjingle_peerconnection_so',
          'type': 'loadable_module',
          'dependencies': [
            'libjingle_peerconnection',
            '<(DEPTH)/third_party/icu/icu.gyp:icuuc',
          ],
          'sources': [
            'app/webrtc/java/jni/peerconnection_jni.cc'
          ],
          'include_dirs': [
            '<(DEPTH)/third_party/libyuv/include',
          ],
          'conditions': [
            ['OS=="linux"', {
              'defines': [
                'HAVE_GTK',
              ],
              'include_dirs': [
                '<(java_home)/include',
                '<(java_home)/include/linux',
              ],
              'link_settings': {
                'libraries': [
                  '<!@(pkg-config --libs-only-l gobject-2.0 gthread-2.0'
                      ' gtk+-2.0)',
                ],
              },
            }],
          ],
        },
        {
          'target_name': 'libjingle_peerconnection_jar',
          'type': 'none',
          'actions': [
            {
              'variables': {
                'java_src_dir': 'app/webrtc/java/src',
                'webrtc_modules_dir': '<(webrtc_root)/modules',
                'build_jar_log': '<(INTERMEDIATE_DIR)/build_jar.log',
                'peerconnection_java_files': [
                  'app/webrtc/java/src/org/webrtc/AudioSource.java',
                  'app/webrtc/java/src/org/webrtc/AudioTrack.java',
                  'app/webrtc/java/src/org/webrtc/DataChannel.java',
                  'app/webrtc/java/src/org/webrtc/IceCandidate.java',
                  'app/webrtc/java/src/org/webrtc/Logging.java',
                  'app/webrtc/java/src/org/webrtc/MediaConstraints.java',
                  'app/webrtc/java/src/org/webrtc/MediaSource.java',
                  'app/webrtc/java/src/org/webrtc/MediaStream.java',
                  'app/webrtc/java/src/org/webrtc/MediaStreamTrack.java',
                  'app/webrtc/java/src/org/webrtc/PeerConnectionFactory.java',
                  'app/webrtc/java/src/org/webrtc/PeerConnection.java',
                  'app/webrtc/java/src/org/webrtc/SdpObserver.java',
                  'app/webrtc/java/src/org/webrtc/StatsObserver.java',
                  'app/webrtc/java/src/org/webrtc/StatsReport.java',
                  'app/webrtc/java/src/org/webrtc/SessionDescription.java',
                  'app/webrtc/java/src/org/webrtc/VideoCapturer.java',
                  'app/webrtc/java/src/org/webrtc/VideoRenderer.java',
                  'app/webrtc/java/src/org/webrtc/VideoSource.java',
                  'app/webrtc/java/src/org/webrtc/VideoTrack.java',
                ],
                # TODO(fischman): extract this into a webrtc gyp var that can be
                # included here, or better yet, build a proper .jar in webrtc
                # and include it here.
                'android_java_files': [
                  'app/webrtc/java/android/org/webrtc/VideoRendererGui.java',
                  'app/webrtc/java/src/org/webrtc/MediaCodecVideoEncoder.java',
                  'app/webrtc/java/src/org/webrtc/MediaCodecVideoDecoder.java',
                  '<(webrtc_modules_dir)/audio_device/android/java/src/org/webrtc/voiceengine/AudioManagerAndroid.java',
                  '<(webrtc_modules_dir)/video_capture/android/java/src/org/webrtc/videoengine/VideoCaptureAndroid.java',
                  '<(webrtc_modules_dir)/video_capture/android/java/src/org/webrtc/videoengine/VideoCaptureDeviceInfoAndroid.java',
                  '<(webrtc_modules_dir)/video_render/android/java/src/org/webrtc/videoengine/ViEAndroidGLES20.java',
                  '<(webrtc_modules_dir)/video_render/android/java/src/org/webrtc/videoengine/ViERenderer.java',
                  '<(webrtc_modules_dir)/video_render/android/java/src/org/webrtc/videoengine/ViESurfaceRenderer.java',
                  '<(webrtc_modules_dir)/audio_device/android/java/src/org/webrtc/voiceengine/WebRtcAudioRecord.java',
                  '<(webrtc_modules_dir)/audio_device/android/java/src/org/webrtc/voiceengine/WebRtcAudioTrack.java',
                ],
              },
              'action_name': 'create_jar',
              'inputs': [
                'build/build_jar.sh',
                '<@(java_files)',
              ],
              'outputs': [
                '<(PRODUCT_DIR)/libjingle_peerconnection.jar',
              ],
              'conditions': [
                ['OS=="android"', {
                  'variables': {
                    'java_files': ['<@(peerconnection_java_files)', '<@(android_java_files)'],
                    'build_classpath': '<(java_src_dir):<(DEPTH)/third_party/android_tools/sdk/platforms/android-<(android_sdk_version)/android.jar',
                  },
                }, {
                  'variables': {
                    'java_files': ['<@(peerconnection_java_files)'],
                    'build_classpath': '<(java_src_dir)',
                  },
                }],
              ],
              'action': [
                'bash', '-ec',
                'mkdir -p <(INTERMEDIATE_DIR) && '
                '{ build/build_jar.sh <(java_home) <@(_outputs) '
                '      <(INTERMEDIATE_DIR)/build_jar.tmp '
                '      <(build_classpath) <@(java_files) '
                '      > <(build_jar_log) 2>&1 || '
                '  { cat <(build_jar_log) ; exit 1; } }'
              ],
            },
          ],
          'dependencies': [
            'libjingle_peerconnection_so',
          ],
        },
      ],
    }],
    ['OS=="ios" or (OS=="mac" and target_arch!="ia32" and mac_sdk>="10.7")', {
      # The >= 10.7 above is required for ARC.
      'targets': [
        {
          'target_name': 'libjingle_peerconnection_objc',
          'type': 'static_library',
          'dependencies': [
            'libjingle_peerconnection',
          ],
          'sources': [
            'app/webrtc/objc/RTCAudioTrack+Internal.h',
            'app/webrtc/objc/RTCAudioTrack.mm',
            'app/webrtc/objc/RTCDataChannel+Internal.h',
            'app/webrtc/objc/RTCDataChannel.mm',
            'app/webrtc/objc/RTCEnumConverter.h',
            'app/webrtc/objc/RTCEnumConverter.mm',
            'app/webrtc/objc/RTCI420Frame+Internal.h',
            'app/webrtc/objc/RTCI420Frame.mm',
            'app/webrtc/objc/RTCICECandidate+Internal.h',
            'app/webrtc/objc/RTCICECandidate.mm',
            'app/webrtc/objc/RTCICEServer+Internal.h',
            'app/webrtc/objc/RTCICEServer.mm',
            'app/webrtc/objc/RTCMediaConstraints+Internal.h',
            'app/webrtc/objc/RTCMediaConstraints.mm',
            'app/webrtc/objc/RTCMediaConstraintsNative.cc',
            'app/webrtc/objc/RTCMediaConstraintsNative.h',
            'app/webrtc/objc/RTCMediaSource+Internal.h',
            'app/webrtc/objc/RTCMediaSource.mm',
            'app/webrtc/objc/RTCMediaStream+Internal.h',
            'app/webrtc/objc/RTCMediaStream.mm',
            'app/webrtc/objc/RTCMediaStreamTrack+Internal.h',
            'app/webrtc/objc/RTCMediaStreamTrack.mm',
            'app/webrtc/objc/RTCOpenGLVideoRenderer.mm',
            'app/webrtc/objc/RTCPair.m',
            'app/webrtc/objc/RTCPeerConnection+Internal.h',
            'app/webrtc/objc/RTCPeerConnection.mm',
            'app/webrtc/objc/RTCPeerConnectionFactory.mm',
            'app/webrtc/objc/RTCPeerConnectionObserver.h',
            'app/webrtc/objc/RTCPeerConnectionObserver.mm',
            'app/webrtc/objc/RTCSessionDescription+Internal.h',
            'app/webrtc/objc/RTCSessionDescription.mm',
            'app/webrtc/objc/RTCStatsReport+Internal.h',
            'app/webrtc/objc/RTCStatsReport.mm',
            'app/webrtc/objc/RTCVideoCapturer+Internal.h',
            'app/webrtc/objc/RTCVideoCapturer.mm',
            'app/webrtc/objc/RTCVideoRenderer+Internal.h',
            'app/webrtc/objc/RTCVideoRenderer.mm',
            'app/webrtc/objc/RTCVideoSource+Internal.h',
            'app/webrtc/objc/RTCVideoSource.mm',
            'app/webrtc/objc/RTCVideoTrack+Internal.h',
            'app/webrtc/objc/RTCVideoTrack.mm',
            'app/webrtc/objc/public/RTCAudioSource.h',
            'app/webrtc/objc/public/RTCAudioTrack.h',
            'app/webrtc/objc/public/RTCDataChannel.h',
            'app/webrtc/objc/public/RTCI420Frame.h',
            'app/webrtc/objc/public/RTCICECandidate.h',
            'app/webrtc/objc/public/RTCICEServer.h',
            'app/webrtc/objc/public/RTCMediaConstraints.h',
            'app/webrtc/objc/public/RTCMediaSource.h',
            'app/webrtc/objc/public/RTCMediaStream.h',
            'app/webrtc/objc/public/RTCMediaStreamTrack.h',
            'app/webrtc/objc/public/RTCOpenGLVideoRenderer.h',
            'app/webrtc/objc/public/RTCPair.h',
            'app/webrtc/objc/public/RTCPeerConnection.h',
            'app/webrtc/objc/public/RTCPeerConnectionDelegate.h',
            'app/webrtc/objc/public/RTCPeerConnectionFactory.h',
            'app/webrtc/objc/public/RTCSessionDescription.h',
            'app/webrtc/objc/public/RTCSessionDescriptionDelegate.h',
            'app/webrtc/objc/public/RTCStatsDelegate.h',
            'app/webrtc/objc/public/RTCStatsReport.h',
            'app/webrtc/objc/public/RTCTypes.h',
            'app/webrtc/objc/public/RTCVideoCapturer.h',
            'app/webrtc/objc/public/RTCVideoRenderer.h',
            'app/webrtc/objc/public/RTCVideoSource.h',
            'app/webrtc/objc/public/RTCVideoTrack.h',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              '<(DEPTH)/talk/app/webrtc/objc/public',
            ],
          },
          'include_dirs': [
            '<(DEPTH)/talk/app/webrtc',
            '<(DEPTH)/talk/app/webrtc/objc',
            '<(DEPTH)/talk/app/webrtc/objc/public',
          ],
          'link_settings': {
            'libraries': [
              '-lstdc++',
            ],
          },
          'xcode_settings': {
            'CLANG_ENABLE_OBJC_ARC': 'YES',
            # common.gypi enables this for mac but we want this to be disabled
            # like it is for ios.
            'CLANG_WARN_OBJC_MISSING_PROPERTY_SYNTHESIS': 'NO',
          },
          'conditions': [
            ['OS=="ios"', {
              'sources': [
                'app/webrtc/objc/RTCEAGLVideoView+Internal.h',
                'app/webrtc/objc/RTCEAGLVideoView.m',
                'app/webrtc/objc/public/RTCEAGLVideoView.h',
              ],
              'link_settings': {
                'xcode_settings': {
                  'OTHER_LDFLAGS': [
                    '-framework CoreGraphics',
                    '-framework GLKit',
                  ],
                },
              },
            }],
            ['OS=="mac"', {
              'sources': [
                'app/webrtc/objc/RTCNSGLVideoView.m',
                'app/webrtc/objc/public/RTCNSGLVideoView.h',
              ],
              'xcode_settings': {
                # Need to build against 10.7 framework for full ARC support
                # on OSX.
                'MACOSX_DEPLOYMENT_TARGET' : '10.7',
              },
              'link_settings': {
                'xcode_settings': {
                  'OTHER_LDFLAGS': [
                    '-framework Cocoa',
                  ],
                },
              },
            }],
          ],
        },  # target libjingle_peerconnection_objc
      ],
    }],
  ],

  'targets': [
    {
      'target_name': 'libjingle',
      'type': 'static_library',
      'dependencies': [
        '<(DEPTH)/third_party/expat/expat.gyp:expat',
        '<(DEPTH)/third_party/jsoncpp/jsoncpp.gyp:jsoncpp',
        '<(webrtc_root)/base/base.gyp:webrtc_base',
      ],
      'export_dependent_settings': [
        '<(DEPTH)/third_party/expat/expat.gyp:expat',
        '<(DEPTH)/third_party/jsoncpp/jsoncpp.gyp:jsoncpp',
      ],
      'sources': [
        'xmllite/qname.cc',
        'xmllite/qname.h',
        'xmllite/xmlbuilder.cc',
        'xmllite/xmlbuilder.h',
        'xmllite/xmlconstants.cc',
        'xmllite/xmlconstants.h',
        'xmllite/xmlelement.cc',
        'xmllite/xmlelement.h',
        'xmllite/xmlnsstack.cc',
        'xmllite/xmlnsstack.h',
        'xmllite/xmlparser.cc',
        'xmllite/xmlparser.h',
        'xmllite/xmlprinter.cc',
        'xmllite/xmlprinter.h',
        'xmpp/asyncsocket.h',
        'xmpp/chatroommodule.h',
        'xmpp/chatroommoduleimpl.cc',
        'xmpp/constants.cc',
        'xmpp/constants.h',
        'xmpp/discoitemsquerytask.cc',
        'xmpp/discoitemsquerytask.h',
        'xmpp/hangoutpubsubclient.cc',
        'xmpp/hangoutpubsubclient.h',
        'xmpp/iqtask.cc',
        'xmpp/iqtask.h',
        'xmpp/jid.cc',
        'xmpp/jid.h',
        'xmpp/module.h',
        'xmpp/moduleimpl.cc',
        'xmpp/moduleimpl.h',
        'xmpp/mucroomconfigtask.cc',
        'xmpp/mucroomconfigtask.h',
        'xmpp/mucroomdiscoverytask.cc',
        'xmpp/mucroomdiscoverytask.h',
        'xmpp/mucroomlookuptask.cc',
        'xmpp/mucroomlookuptask.h',
        'xmpp/mucroomuniquehangoutidtask.cc',
        'xmpp/mucroomuniquehangoutidtask.h',
        'xmpp/pingtask.cc',
        'xmpp/pingtask.h',
        'xmpp/plainsaslhandler.h',
        'xmpp/presenceouttask.cc',
        'xmpp/presenceouttask.h',
        'xmpp/presencereceivetask.cc',
        'xmpp/presencereceivetask.h',
        'xmpp/presencestatus.cc',
        'xmpp/presencestatus.h',
        'xmpp/prexmppauth.h',
        'xmpp/pubsub_task.cc',
        'xmpp/pubsub_task.h',
        'xmpp/pubsubclient.cc',
        'xmpp/pubsubclient.h',
        'xmpp/pubsubstateclient.cc',
        'xmpp/pubsubstateclient.h',
        'xmpp/pubsubtasks.cc',
        'xmpp/pubsubtasks.h',
        'xmpp/receivetask.cc',
        'xmpp/receivetask.h',
        'xmpp/rostermodule.h',
        'xmpp/rostermoduleimpl.cc',
        'xmpp/rostermoduleimpl.h',
        'xmpp/saslcookiemechanism.h',
        'xmpp/saslhandler.h',
        'xmpp/saslmechanism.cc',
        'xmpp/saslmechanism.h',
        'xmpp/saslplainmechanism.h',
        'xmpp/xmppauth.cc',
        'xmpp/xmppauth.h',
        'xmpp/xmppclient.cc',
        'xmpp/xmppclient.h',
        'xmpp/xmppclientsettings.h',
        'xmpp/xmppengine.h',
        'xmpp/xmppengineimpl.cc',
        'xmpp/xmppengineimpl.h',
        'xmpp/xmppengineimpl_iq.cc',
        'xmpp/xmpplogintask.cc',
        'xmpp/xmpplogintask.h',
        'xmpp/xmpppump.cc',
        'xmpp/xmpppump.h',
        'xmpp/xmppsocket.cc',
        'xmpp/xmppsocket.h',
        'xmpp/xmppstanzaparser.cc',
        'xmpp/xmppstanzaparser.h',
        'xmpp/xmpptask.cc',
        'xmpp/xmpptask.h',
        'xmpp/xmppthread.cc',
        'xmpp/xmppthread.h',
      ],
    },  # target libjingle
    {
      'target_name': 'libjingle_sound',
      'type': 'static_library',
      'dependencies': [
        'libjingle',
      ],
      'sources': [
        'sound/automaticallychosensoundsystem.h',
        'sound/nullsoundsystem.cc',
        'sound/nullsoundsystem.h',
        'sound/nullsoundsystemfactory.cc',
        'sound/nullsoundsystemfactory.h',
        'sound/platformsoundsystem.cc',
        'sound/platformsoundsystem.h',
        'sound/platformsoundsystemfactory.cc',
        'sound/platformsoundsystemfactory.h',
        'sound/sounddevicelocator.h',
        'sound/soundinputstreaminterface.h',
        'sound/soundoutputstreaminterface.h',
        'sound/soundsystemfactory.h',
        'sound/soundsysteminterface.cc',
        'sound/soundsysteminterface.h',
        'sound/soundsystemproxy.cc',
        'sound/soundsystemproxy.h',
      ],
      'conditions': [
        ['OS=="linux"', {
          'sources': [
            'sound/alsasoundsystem.cc',
            'sound/alsasoundsystem.h',
            'sound/alsasymboltable.cc',
            'sound/alsasymboltable.h',
            'sound/linuxsoundsystem.cc',
            'sound/linuxsoundsystem.h',
            'sound/pulseaudiosoundsystem.cc',
            'sound/pulseaudiosoundsystem.h',
            'sound/pulseaudiosymboltable.cc',
            'sound/pulseaudiosymboltable.h',
          ],
        }],
      ],
    },  # target libjingle_sound
    {
      'target_name': 'libjingle_media',
      'type': 'static_library',
      'include_dirs': [
        # TODO(jiayl): move this into the direct_dependent_settings of
        # usrsctp.gyp.
        '<(DEPTH)/third_party/usrsctp',
      ],
      'dependencies': [
        '<(DEPTH)/third_party/libyuv/libyuv.gyp:libyuv',
        '<(DEPTH)/third_party/usrsctp/usrsctp.gyp:usrsctplib',
        '<(webrtc_root)/modules/modules.gyp:video_capture_module',
        '<(webrtc_root)/modules/modules.gyp:video_render_module',
        '<(webrtc_root)/webrtc.gyp:webrtc',
        '<(webrtc_root)/voice_engine/voice_engine.gyp:voice_engine',
        '<(webrtc_root)/system_wrappers/source/system_wrappers.gyp:system_wrappers',
        '<(webrtc_root)/system_wrappers/source/system_wrappers.gyp:field_trial_default',
        'libjingle',
        'libjingle_sound',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(DEPTH)/third_party/libyuv/include',
        ],
      },
      'sources': [
        'media/base/audioframe.h',
        'media/base/audiorenderer.h',
        'media/base/capturemanager.cc',
        'media/base/capturemanager.h',
        'media/base/capturerenderadapter.cc',
        'media/base/capturerenderadapter.h',
        'media/base/codec.cc',
        'media/base/codec.h',
        'media/base/constants.cc',
        'media/base/constants.h',
        'media/base/cpuid.cc',
        'media/base/cpuid.h',
        'media/base/cryptoparams.h',
        'media/base/device.h',
        'media/base/fakescreencapturerfactory.h',
        'media/base/filemediaengine.cc',
        'media/base/filemediaengine.h',
        'media/base/hybriddataengine.h',
        'media/base/hybridvideoengine.cc',
        'media/base/hybridvideoengine.h',
        'media/base/mediachannel.h',
        'media/base/mediacommon.h',
        'media/base/mediaengine.cc',
        'media/base/mediaengine.h',
        'media/base/rtpdataengine.cc',
        'media/base/rtpdataengine.h',
        'media/base/rtpdump.cc',
        'media/base/rtpdump.h',
        'media/base/rtputils.cc',
        'media/base/rtputils.h',
        'media/base/screencastid.h',
        'media/base/streamparams.cc',
        'media/base/streamparams.h',
        'media/base/videoadapter.cc',
        'media/base/videoadapter.h',
        'media/base/videocapturer.cc',
        'media/base/videocapturer.h',
        'media/base/videocapturerfactory.h',
        'media/base/videocommon.cc',
        'media/base/videocommon.h',
        'media/base/videoframe.cc',
        'media/base/videoframe.h',
        'media/base/videoframefactory.h',
        'media/base/videoprocessor.h',
        'media/base/videorenderer.h',
        'media/base/voiceprocessor.h',
        'media/base/yuvframegenerator.cc',
        'media/base/yuvframegenerator.h',
        'media/devices/deviceinfo.h',
        'media/devices/devicemanager.cc',
        'media/devices/devicemanager.h',
        'media/devices/dummydevicemanager.h',
        'media/devices/filevideocapturer.cc',
        'media/devices/filevideocapturer.h',
        'media/devices/videorendererfactory.h',
        'media/devices/yuvframescapturer.cc',
        'media/devices/yuvframescapturer.h',
        'media/other/linphonemediaengine.h',
        'media/sctp/sctpdataengine.cc',
        'media/sctp/sctpdataengine.h',
        'media/webrtc/webrtccommon.h',
        'media/webrtc/webrtcexport.h',
        'media/webrtc/webrtcmediaengine.cc',
        'media/webrtc/webrtcmediaengine.h',
        'media/webrtc/webrtcpassthroughrender.cc',
        'media/webrtc/webrtcpassthroughrender.h',
        'media/webrtc/webrtctexturevideoframe.cc',
        'media/webrtc/webrtctexturevideoframe.h',
        'media/webrtc/webrtcvideocapturer.cc',
        'media/webrtc/webrtcvideocapturerfactory.h',
        'media/webrtc/webrtcvideocapturerfactory.cc',
        'media/webrtc/webrtcvideocapturer.h',
        'media/webrtc/webrtcvideodecoderfactory.h',
        'media/webrtc/webrtcvideoencoderfactory.h',
        'media/webrtc/webrtcvideoengine.cc',
        'media/webrtc/webrtcvideoengine.h',
        'media/webrtc/webrtcvideoengine2.cc',
        'media/webrtc/webrtcvideoengine2.h',
        'media/webrtc/webrtcvideoframe.cc',
        'media/webrtc/webrtcvideoframe.h',
        'media/webrtc/webrtcvideoframefactory.cc',
        'media/webrtc/webrtcvideoframefactory.h',
        'media/webrtc/webrtcvie.h',
        'media/webrtc/webrtcvoe.h',
        'media/webrtc/webrtcvoiceengine.cc',
        'media/webrtc/webrtcvoiceengine.h',
      ],
      'conditions': [
        ['OS=="linux"', {
          'sources': [
            'media/devices/gtkvideorenderer.cc',
            'media/devices/gtkvideorenderer.h',
            'media/devices/libudevsymboltable.cc',
            'media/devices/libudevsymboltable.h',
            'media/devices/linuxdeviceinfo.cc',
            'media/devices/linuxdevicemanager.cc',
            'media/devices/linuxdevicemanager.h',
            'media/devices/v4llookup.cc',
            'media/devices/v4llookup.h',
          ],
          'include_dirs': [
            'third_party/libudev'
          ],
          'cflags': [
            '<!@(pkg-config --cflags gobject-2.0 gthread-2.0 gtk+-2.0)',
          ],
          'libraries': [
            '-lrt',
            '-lXext',
            '-lX11',
          ],
        }],
        ['OS=="win"', {
          'sources': [
            'media/devices/gdivideorenderer.cc',
            'media/devices/gdivideorenderer.h',
            'media/devices/win32deviceinfo.cc',
            'media/devices/win32devicemanager.cc',
            'media/devices/win32devicemanager.h',
          ],
          'msvs_settings': {
            'VCLibrarianTool': {
              'AdditionalDependencies': [
                'd3d9.lib',
                'gdi32.lib',
                'strmiids.lib',
                'winmm.lib',
              ],
            },
          },
        }],
        ['OS=="mac"', {
          'sources': [
            'media/devices/macdeviceinfo.cc',
            'media/devices/macdevicemanager.cc',
            'media/devices/macdevicemanager.h',
            'media/devices/macdevicemanagermm.mm',
          ],
          'conditions': [
            ['target_arch=="ia32"', {
              'sources': [
                'media/devices/carbonvideorenderer.cc',
                'media/devices/carbonvideorenderer.h',
              ],
              'link_settings': {
                'xcode_settings': {
                  'OTHER_LDFLAGS': [
                    '-framework Carbon',
                  ],
                },
              },
            }],
          ],
          'xcode_settings': {
            'WARNING_CFLAGS': [
              # TODO(ronghuawu): Update macdevicemanager.cc to stop using
              # deprecated functions and remove this flag.
              '-Wno-deprecated-declarations',
            ],
          },
          'link_settings': {
            'xcode_settings': {
              'OTHER_LDFLAGS': [
                '-framework Cocoa',
                '-framework CoreAudio',
                '-framework CoreVideo',
                '-framework OpenGL',
                '-framework QTKit',
              ],
            },
          },
        }],
        ['OS=="ios"', {
          'sources': [
            'media/devices/mobiledevicemanager.cc',
          ],
          'include_dirs': [
            # TODO(sjlee) Remove when vp8 is building for iOS.  vp8 pulls in
            # libjpeg which pulls in libyuv which currently disabled.
            '../third_party/libyuv/include',
          ],
        }],
        ['OS=="android"', {
          'sources': [
            'media/devices/mobiledevicemanager.cc',
          ],
        }],
      ],
    },  # target libjingle_media
    {
      'target_name': 'libjingle_p2p',
      'type': 'static_library',
      'dependencies': [
        '<(DEPTH)/third_party/libsrtp/libsrtp.gyp:libsrtp',
        'libjingle',
        'libjingle_media',
      ],
      'include_dirs': [
        '<(DEPTH)/testing/gtest/include',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(DEPTH)/testing/gtest/include',
        ],
      },
      'sources': [
        'p2p/base/asyncstuntcpsocket.cc',
        'p2p/base/asyncstuntcpsocket.h',
        'p2p/base/basicpacketsocketfactory.cc',
        'p2p/base/basicpacketsocketfactory.h',
        'p2p/base/candidate.h',
        'p2p/base/common.h',
        'p2p/base/constants.cc',
        'p2p/base/constants.h',
        'p2p/base/dtlstransportchannel.cc',
        'p2p/base/dtlstransportchannel.h',
        'p2p/base/p2ptransport.cc',
        'p2p/base/p2ptransport.h',
        'p2p/base/p2ptransportchannel.cc',
        'p2p/base/p2ptransportchannel.h',
        'p2p/base/packetsocketfactory.h',
        'p2p/base/parsing.cc',
        'p2p/base/parsing.h',
        'p2p/base/port.cc',
        'p2p/base/port.h',
        'p2p/base/portallocator.cc',
        'p2p/base/portallocator.h',
        'p2p/base/portallocatorsessionproxy.cc',
        'p2p/base/portallocatorsessionproxy.h',
        'p2p/base/portinterface.h',
        'p2p/base/portproxy.cc',
        'p2p/base/portproxy.h',
        'p2p/base/pseudotcp.cc',
        'p2p/base/pseudotcp.h',
        'p2p/base/rawtransport.cc',
        'p2p/base/rawtransport.h',
        'p2p/base/rawtransportchannel.cc',
        'p2p/base/rawtransportchannel.h',
        'p2p/base/relayport.cc',
        'p2p/base/relayport.h',
        'p2p/base/relayserver.cc',
        'p2p/base/relayserver.h',
        'p2p/base/session.cc',
        'p2p/base/session.h',
        'p2p/base/sessionclient.h',
        'p2p/base/sessiondescription.cc',
        'p2p/base/sessiondescription.h',
        'p2p/base/sessionid.h',
        'p2p/base/sessionmanager.cc',
        'p2p/base/sessionmanager.h',
        'p2p/base/sessionmessages.cc',
        'p2p/base/sessionmessages.h',
        'p2p/base/stun.cc',
        'p2p/base/stun.h',
        'p2p/base/stunport.cc',
        'p2p/base/stunport.h',
        'p2p/base/stunrequest.cc',
        'p2p/base/stunrequest.h',
        'p2p/base/stunserver.cc',
        'p2p/base/stunserver.h',
        'p2p/base/tcpport.cc',
        'p2p/base/tcpport.h',
        'p2p/base/transport.cc',
        'p2p/base/transport.h',
        'p2p/base/transportchannel.cc',
        'p2p/base/transportchannel.h',
        'p2p/base/transportchannelimpl.h',
        'p2p/base/transportchannelproxy.cc',
        'p2p/base/transportchannelproxy.h',
        'p2p/base/transportdescription.cc',
        'p2p/base/transportdescription.h',
        'p2p/base/transportdescriptionfactory.cc',
        'p2p/base/transportdescriptionfactory.h',
        'p2p/base/transportinfo.h',
        'p2p/base/turnport.cc',
        'p2p/base/turnport.h',
        'p2p/base/turnserver.cc',
        'p2p/base/turnserver.h',
        'p2p/base/udpport.h',
        'p2p/client/autoportallocator.h',
        'p2p/client/basicportallocator.cc',
        'p2p/client/basicportallocator.h',
        'p2p/client/connectivitychecker.cc',
        'p2p/client/connectivitychecker.h',
        'p2p/client/httpportallocator.cc',
        'p2p/client/httpportallocator.h',
        'p2p/client/sessionmanagertask.h',
        'p2p/client/sessionsendtask.h',
        'p2p/client/socketmonitor.cc',
        'p2p/client/socketmonitor.h',
        'session/tunnel/pseudotcpchannel.cc',
        'session/tunnel/pseudotcpchannel.h',
        'session/tunnel/tunnelsessionclient.cc',
        'session/tunnel/tunnelsessionclient.h',
        'session/tunnel/securetunnelsessionclient.cc',
        'session/tunnel/securetunnelsessionclient.h',
        'session/media/audiomonitor.cc',
        'session/media/audiomonitor.h',
        'session/media/bundlefilter.cc',
        'session/media/bundlefilter.h',
        'session/media/call.cc',
        'session/media/call.h',
        'session/media/channel.cc',
        'session/media/channel.h',
        'session/media/channelmanager.cc',
        'session/media/channelmanager.h',
        'session/media/currentspeakermonitor.cc',
        'session/media/currentspeakermonitor.h',
        'session/media/mediamessages.cc',
        'session/media/mediamessages.h',
        'session/media/mediamonitor.cc',
        'session/media/mediamonitor.h',
        'session/media/mediarecorder.cc',
        'session/media/mediarecorder.h',
        'session/media/mediasession.cc',
        'session/media/mediasession.h',
        'session/media/mediasessionclient.cc',
        'session/media/mediasessionclient.h',
        'session/media/mediasink.h',
        'session/media/rtcpmuxfilter.cc',
        'session/media/rtcpmuxfilter.h',
        'session/media/soundclip.cc',
        'session/media/soundclip.h',
        'session/media/srtpfilter.cc',
        'session/media/srtpfilter.h',
        'session/media/typingmonitor.cc',
        'session/media/typingmonitor.h',
        'session/media/voicechannel.h',
      ],
    },  # target libjingle_p2p
    {
      'target_name': 'libjingle_peerconnection',
      'type': 'static_library',
      'dependencies': [
        'libjingle',
        'libjingle_media',
        'libjingle_p2p',
      ],
      'sources': [
        'app/webrtc/audiotrack.cc',
        'app/webrtc/audiotrack.h',
        'app/webrtc/audiotrackrenderer.cc',
        'app/webrtc/audiotrackrenderer.h',
        'app/webrtc/datachannel.cc',
        'app/webrtc/datachannel.h',
        'app/webrtc/datachannelinterface.h',
        'app/webrtc/dtmfsender.cc',
        'app/webrtc/dtmfsender.h',
        'app/webrtc/dtmfsenderinterface.h',
        'app/webrtc/fakeportallocatorfactory.h',
        'app/webrtc/jsep.h',
        'app/webrtc/jsepicecandidate.cc',
        'app/webrtc/jsepicecandidate.h',
        'app/webrtc/jsepsessiondescription.cc',
        'app/webrtc/jsepsessiondescription.h',
        'app/webrtc/localaudiosource.cc',
        'app/webrtc/localaudiosource.h',
        'app/webrtc/mediaconstraintsinterface.cc',
        'app/webrtc/mediaconstraintsinterface.h',
        'app/webrtc/mediastream.cc',
        'app/webrtc/mediastream.h',
        'app/webrtc/mediastreamhandler.cc',
        'app/webrtc/mediastreamhandler.h',
        'app/webrtc/mediastreaminterface.h',
        'app/webrtc/mediastreamprovider.h',
        'app/webrtc/mediastreamproxy.h',
        'app/webrtc/mediastreamsignaling.cc',
        'app/webrtc/mediastreamsignaling.h',
        'app/webrtc/mediastreamtrack.h',
        'app/webrtc/mediastreamtrackproxy.h',
        'app/webrtc/notifier.h',
        'app/webrtc/peerconnection.cc',
        'app/webrtc/peerconnection.h',
        'app/webrtc/peerconnectionfactory.cc',
        'app/webrtc/peerconnectionfactory.h',
        'app/webrtc/peerconnectioninterface.h',
        'app/webrtc/peerconnectionproxy.h',
        'app/webrtc/portallocatorfactory.cc',
        'app/webrtc/portallocatorfactory.h',
        'app/webrtc/proxy.h',
        'app/webrtc/remoteaudiosource.cc',
        'app/webrtc/remoteaudiosource.h',
        'app/webrtc/remotevideocapturer.cc',
        'app/webrtc/remotevideocapturer.h',
        'app/webrtc/sctputils.cc',
        'app/webrtc/sctputils.h',
        'app/webrtc/statscollector.cc',
        'app/webrtc/statscollector.h',
        'app/webrtc/statstypes.h',
        'app/webrtc/streamcollection.h',
        'app/webrtc/videosource.cc',
        'app/webrtc/videosource.h',
        'app/webrtc/videosourceinterface.h',
        'app/webrtc/videosourceproxy.h',
        'app/webrtc/videotrack.cc',
        'app/webrtc/videotrack.h',
        'app/webrtc/videotrackrenderers.cc',
        'app/webrtc/videotrackrenderers.h',
        'app/webrtc/webrtcsdp.cc',
        'app/webrtc/webrtcsdp.h',
        'app/webrtc/webrtcsession.cc',
        'app/webrtc/webrtcsession.h',
        'app/webrtc/webrtcsessiondescriptionfactory.cc',
        'app/webrtc/webrtcsessiondescriptionfactory.h',
      ],
    },  # target libjingle_peerconnection
  ],
}

module.exports = function(grunt) {
  grunt.initConfig({
    htmllint: {
      all: {
        options: {
          ignore : [
            /Section lacks heading/,
            /cc:attributionURL/,
            /Attribute “rel” not allowed on element “span”/,
            /Consider using the “h1” element/

          ]
        },
        src : '_site/**/*.html'
      }
    }
  });
  grunt.loadNpmTasks('grunt-html');
  grunt.registerTask('test', ['htmllint']);
};

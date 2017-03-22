/*
Example files
*/

clust_options = {};
clust_options.protein_class = 'KIN';
clust_options.data_type = 'ccle';

full_names = {};
full_names.ccle = 'my_CCLE_exp';
full_names.gtex = 'my_gtex_Moshe_2017_exp';
full_names.encode = 'ENCODE_TF_targets';
full_names.chea = 'ChEA_TF_targets';

$("#dropdown_menu_1 li a").click(function(){

  $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
  $(this).parents(".dropdown").find('.btn').val($(this).data('value'));

  console.log('change clustergram protein class')

  // update global clust_options and rerun make_clust
  clust_options.protein_class = d3.select(this).attr('data-value');
  make_clust();

});

$("#dropdown_menu_2 li a").click(function(){

  $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
  $(this).parents(".dropdown").find('.btn').val($(this).data('value'));

  console.log('change clustergram data type')

  clust_options.data_type = d3.select(this).attr('data-value');
  make_clust();

});

var hzome = ini_hzome();

// initial view
make_clust();

// var about_string = 'Zoom, scroll, and click buttons to interact with the clustergram. <a href="http://amp.pharm.mssm.edu/clustergrammer/help"> <i class="fa fa-question-circle" aria-hidden="true"></i> </a>';

function make_clust(){

  var data_name = full_names[clust_options.data_type];
  var inst_network = data_name + '_' + clust_options.protein_class + '.json';

  console.log(inst_network)

  // clear out old visualization elements
  d3.selectAll('#container-id-1 div').remove();

  // <h1 class='wait_message'>Please wait ...</h1>

  d3.select('#container-id-1')
    .append('h1')
    .classed('wait_message', true)
    .html('Please wait ...');

  d3.json('json/'+inst_network, function(network_data){

      // define arguments object
      var args = {
        root: '#container-id-1',
        'network_data': network_data,
        // 'about':about_string,
        'row_tip_callback':hzome.gene_info,
        'col_tip_callback':test_col_callback,
        'tile_tip_callback':test_tile_callback,
        'dendro_callback':dendro_callback,
        // 'matrix_update_callback':matrix_update_callback,
        'sidebar_width':150,
        // 'ini_view':{'N_row_var':20}
      };

      resize_container(args);

      d3.select(window).on('resize',function(){
        resize_container(args);
        cgm.resize_viz();
      });

      cgm = Clustergrammer(args);

      check_setup_enrichr(cgm);

      d3.select(cgm.params.root + ' .wait_message').remove();

  });

}

function matrix_update_callback(){

  if (genes_were_found[this.root]){
    enr_obj[this.root].clear_enrichr_results(false);
  }
}

function test_tile_callback(tile_data){
  var row_name = tile_data.row_name;
  var col_name = tile_data.col_name;

}

function test_col_callback(col_data){
  var col_name = col_data.name;
}

function dendro_callback(inst_selection){

  var inst_rc;
  var inst_data = inst_selection.__data__;

  // toggle enrichr export section
  if (inst_data.inst_rc === 'row'){
    d3.select('.enrichr_export_section')
      .style('display', 'block');
  } else {
    d3.select('.enrichr_export_section')
      .style('display', 'none');
  }

}

function resize_container(args){

  var top_section = 55

  var screen_width = window.innerWidth;
  var screen_height = window.innerHeight - 20 - top_section;

  d3.select(args.root)
    .style('width', screen_width+'px')
    .style('height', screen_height+'px');
    // .style('margin-top', top_section+'px');
}